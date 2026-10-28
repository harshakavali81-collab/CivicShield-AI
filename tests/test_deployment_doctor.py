"""Deployment diagnostics must fail closed without printing credentials."""
from __future__ import annotations
from backend.app.reviewer_identity import actor_reference
from backend.app.oidc import validate_production_configuration
from scripts.doctor import evaluate
import pytest

SAMPLE_SECRET = "not-a-real-key-12345678901234567890abcdef"
BASE = {
    "APP_ENV": "production", "AUTH_MODE": "oidc",
    "DATABASE_URL": "postgresql+psycopg://db-user:example-secret@db.local:5432/civicshield",
    "INCIDENT_SUBMISSIONS_ENABLED": "false",
    "OIDC_ISSUER": "https://idp.example.org",
    "OIDC_AUDIENCE": "civicshield-api",
    "OIDC_JWKS_URL": "https://idp.example.org/jwks",
    "CORS_ORIGINS": "https://demo.example.org",
    "AUDIT_HASH_SECRET": SAMPLE_SECRET,
}

def test_preflight_accepts_technical_configuration_without_certifying_provider():
    result = evaluate("production", BASE, executable=lambda _: "/mock/python")
    assert result["configuration_pass"] is True
    assert result["official_hazard_feed_verified"] is False
    assert result["live_cloud_deployment_verified"] is False
    assert result["scientific_prediction_validated"] is False
    assert "example-secret" not in str(result)
    assert SAMPLE_SECRET not in str(result)

@pytest.mark.parametrize("name,invalid", [
    ("APP_ENV", "local"),
    ("AUTH_MODE", "demo_key"),
    ("DATABASE_URL", "sqlite:///test.db"),
    ("OIDC_ISSUER", "http://insecure.example"),
    ("OIDC_JWKS_URL", "http://insecure.example/keys"),
    ("CORS_ORIGINS", "*"),
    ("CORS_ORIGINS", "http://insecure.example"),
    ("CORS_ORIGINS", "https://trusted.example/path"),
    ("CORS_ORIGINS", "https://trusted.example?bad=true"),
    ("CORS_ORIGINS", "https://user:pass@trusted.example"),
    ("OIDC_AUDIENCE", ""),
    ("AUDIT_HASH_SECRET", "short"),
    ("INCIDENT_SUBMISSIONS_ENABLED", "true"),
])
def test_production_requires_safe_configuration(name, invalid):
    env = {**BASE, name: invalid}
    result = evaluate("production", env, executable=lambda _: "/mock/python")
    assert result["configuration_pass"] is False
    assert result["errors"]
    assert SAMPLE_SECRET not in str(result)

def test_doctor_local_reports_advisory_not_production_certification():
    report = evaluate("local", {"INCIDENT_SUBMISSIONS_ENABLED": "false"}, executable=lambda _: None)
    assert report["configuration_pass"] is True
    assert report["advisories"]
    assert report["real_identity_provider_verified"] is False

def test_actor_hmac_has_secret_separation_and_stability(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    claims = {"iss": "https://idp.example.org", "sub": "user-test"}
    monkeypatch.setenv("AUDIT_HASH_SECRET", SAMPLE_SECRET)
    first = actor_reference(claims)
    assert first.startswith("oidc_")
    assert "user-test" not in first
    assert first == actor_reference(claims)
    monkeypatch.setenv("AUDIT_HASH_SECRET", "separate-key-of-adequate-length-123456789")
    assert actor_reference(claims) != first
    monkeypatch.setenv("AUDIT_HASH_SECRET", "short")
    with pytest.raises(RuntimeError,match="secret"):
        actor_reference(claims)

def test_production_validator_requires_audit_secret(monkeypatch):
    for k,v in BASE.items():
        monkeypatch.setenv(k,v)
    validate_production_configuration()
    monkeypatch.setenv("AUDIT_HASH_SECRET","")
    with pytest.raises(RuntimeError,match="AUDIT_HASH_SECRET"):
        validate_production_configuration()
