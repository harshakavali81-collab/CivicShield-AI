"""Official-source validation, OIDC role logic and spatial/temporal holdout safeguards."""
from datetime import datetime, timedelta, timezone
import json
import os
import jwt
import pandas as pd
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from backend.app.oidc import (
    _responder_role, _configuration, validate_oidc_token,
    validate_production_configuration,
)
from civicshield.ingestion.imd_official import parse_warning, normalize_response
from civicshield.ml.validate_external import validate

def imd_record():
    now = datetime.now(timezone.utc) - timedelta(hours=1)
    return {
        "Obj_id": "573", "Date": now.strftime("%Y-%m-%d"),
        "UTC": now.strftime("%H%M"), "District": "DEMO DISTRICT",
        **{f"Day_{n}": "2,4" for n in range(1,6)},
        **{f"Day{n}_Color": "2" for n in range(1,6)},
    }

def test_imd_code_color_provenance():
    record = parse_warning(imd_record())
    assert record["official_api_response"] is True
    assert record["source_type"] == "imd_direct_api_response"
    assert record["days"][0]["color"] == "orange"
    assert record["days"][0]["phenomena"] == ["heavy rain", "thunderstorm/lightning"]
    assert "api.imd.gov.in" in record["original_source_url"]
    assert normalize_response([imd_record()], 573)["district_id"] == "573"

def test_imd_schema_error_and_staleness_fail_closed():
    payload = imd_record()
    payload["Day3_Color"] = "999"
    with pytest.raises(ValueError):
        parse_warning(payload)
    stale = imd_record()
    yesterday = datetime.now(timezone.utc) - timedelta(days=5)
    stale["Date"] = yesterday.strftime("%Y-%m-%d")
    stale["UTC"] = yesterday.strftime("%H%M")
    with pytest.raises(ValueError):
        parse_warning(stale)

def test_imd_disabled_no_provider_call(client, monkeypatch):
    monkeypatch.setenv("IMD_API_ENABLED", "false")
    r = client.get("/api/v1/official/imd/district-warning?district_id=573")
    assert r.status_code == 503
    status = client.get("/api/v1/official/integration-status").json()
    assert status["imd"]["enabled"] is False
    assert status["cwc"]["api_connected"] is False

def test_oidc_requires_explicit_configuration(monkeypatch):
    monkeypatch.setenv("OIDC_ISSUER", "http://bad-idp.example/")
    monkeypatch.setenv("OIDC_AUDIENCE", "civicshield-api")
    monkeypatch.setenv("OIDC_JWKS_URL", "https://bad-idp.example/jwks")
    with pytest.raises(RuntimeError):
        _configuration()

def test_oidc_signature_audience_and_role(monkeypatch):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key()
    issuer = "https://issuer.example.org"
    monkeypatch.setenv("OIDC_ISSUER", issuer)
    monkeypatch.setenv("OIDC_AUDIENCE", "civicshield-api")
    monkeypatch.setenv("OIDC_JWKS_URL", issuer + "/jwks.json")
    monkeypatch.setenv("OIDC_ROLES_CLAIM", "roles")
    import backend.app.oidc as module
    class MockKey: pass
    class MockClient:
        def get_signing_key_from_jwt(self, token):
            x = MockKey()
            x.key = public
            return x
    monkeypatch.setattr(module, "_jwk_client", lambda _: MockClient())
    now = int(datetime.now(timezone.utc).timestamp())
    claims = {"iss":issuer,"aud":"civicshield-api","sub":"reviewer-123",
      "exp":now+1800,"iat":now,"roles":["civicshield-responder"]}
    token = jwt.encode(claims, key, algorithm="RS256")
    valid = validate_oidc_token(token)
    assert _responder_role(valid)
    assert not _responder_role({**valid, "roles":["reader"]})
    bad = jwt.encode({**claims,"aud":"another-service"},key,algorithm="RS256")
    with pytest.raises(jwt.InvalidAudienceError):
        validate_oidc_token(bad)

def test_production_refuses_demo_security(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("AUTH_MODE", "demo_key")
    with pytest.raises(RuntimeError, match="OIDC"):
        validate_production_configuration()

def test_spatiotemporal_external_validation(tmp_path):
    # Synthetic rows exercise code only; do NOT represent scientific validation.
    from datetime import timedelta
    dates = pd.date_range("2025-01-01", periods=110, freq="D", tz="UTC")
    rows = []
    for district in ("Alpha","Bravo","Charlie","Delta"):
        for i, dt in enumerate(dates):
            rows.append({"district":district,"observed_at":dt.isoformat(),
                "rainfall_24h_mm":20+(i%15)*3,"temperature_c":21+(i%9),
                "humidity_pct":55+(i%11),"risk_label":i%2})
    path = tmp_path / "synthetic.csv"
    pd.DataFrame(rows).to_csv(path,index=False)
    output = tmp_path / "validation.json"
    result = validate(str(path),str(output))
    assert result["training_rows"] > 100
    assert result["heldout_district"] == "Delta"
    assert result["temporal_holdout"]["samples"] >= 30
    assert result["geographic_holdout"]["samples"] == 110
    assert result["passes_operational_validation"] is False
    assert output.is_file()

def test_external_validation_rejects_small_data(tmp_path):
    path=tmp_path/"few.csv"
    pd.DataFrame([{"observed_at":"2025-01-01", "district":"A","risk_label":1,
        "rainfall_24h_mm":5,"temperature_c":29,"humidity_pct":75}]).to_csv(path,index=False)
    with pytest.raises(ValueError,match="300"):
        validate(str(path),str(tmp_path/"result.json"))
