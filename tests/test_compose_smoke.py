"""Check the self-contained stack acceptance CLI contract without Docker.

Real Docker Compose integration runs separately as a GitHub Actions job.
"""
from __future__ import annotations
import json
from io import BytesIO
from unittest.mock import patch
from scripts import smoke_compose


class FakeResponse:
    def __init__(self, body, content_type="application/json"):
        self.status = 200
        self.headers = {"Content-Type": content_type}
        self.body = body if isinstance(body, bytes) else json.dumps(body).encode()
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, length=None): return self.body


def test_compose_contract_checks_proxy_and_safe_provenance():
    seen = []
    cases = {
        "/": FakeResponse(b'<html>CivicShield <script src="/assets/index.js"></script></html>', "text/html"),
        "/api/health": FakeResponse({"mode": "research_demo"}),
        "/api/ready": FakeResponse({"status": "ready", "official_emergency_service": False}),
        "/api/v1/alerts": FakeResponse({"connection_state": "not_connected", "official_alerts": []}),
        "/api/v1/demo/scenario": FakeResponse({
            "samples": [{}] * 24, "is_synthetic": True,
            "official_data_connected": False, "database_reports_created": 0,
        }),
        "/api/v1/analytics/summary": FakeResponse({"report_total": 0}),
        "/api/v1/risk/estimate": FakeResponse({
            "risk_level": "unavailable", "is_official_warning": False,
        }),
        "/portfolio-demo-check": FakeResponse(b"<html>CivicShield</html>", "text/html"),
    }
    def opener(req, timeout=12):
        seen.append(req)
        return cases[req.full_url.replace("http://127.0.0.1:5173", "")]
    with patch.object(smoke_compose, "urlopen", side_effect=opener):
        result = smoke_compose.check("http://127.0.0.1:5173", require_empty_db=True)
    assert result["result"] == "PASS"
    assert result["checks"] == 8
    assert result["incident_database_modified"] is False
    assert len(seen) == 8
    payload = seen[6].data.decode("utf-8")
    assert seen[6].get_method() == "POST"
    assert json.loads(payload)["forecast_age_hours"] == 7


def test_acceptance_fails_if_alerts_fabricated():
    cases = {
        "/": FakeResponse(b'<html>CivicShield <script src="/assets/a.js"></script></html>', "text/html"),
        "/api/health": FakeResponse({"mode": "research_demo"}),
        "/api/ready": FakeResponse({"status": "ready", "official_emergency_service": False}),
        "/api/v1/alerts": FakeResponse({"connection_state": "connected", "official_alerts": [{"fake": True}]}),
    }
    def opener(req, timeout=12):
        return cases[req.full_url.replace("http://127.0.0.1:5173", "")]
    with patch.object(smoke_compose, "urlopen", side_effect=opener):
        import pytest
        with pytest.raises(AssertionError):
            smoke_compose.check("http://127.0.0.1:5173")


def test_acceptance_can_run_on_a_previously_used_local_demo():
    cases = {
        "/": FakeResponse(b'<html>CivicShield <script src="/assets/a.js"></script></html>', "text/html"),
        "/api/health": FakeResponse({"mode":"research_demo"}),
        "/api/ready": FakeResponse({"status":"ready", "official_emergency_service": False}),
        "/api/v1/alerts": FakeResponse({"connection_state":"not_connected","official_alerts":[]}),
        "/api/v1/demo/scenario": FakeResponse({
            "samples":[{}]*24,"is_synthetic":True,
            "official_data_connected":False, "database_reports_created":0,
        }),
        "/api/v1/analytics/summary": FakeResponse({"report_total": 3}),
        "/api/v1/risk/estimate": FakeResponse({"risk_level":"unavailable","is_official_warning":False}),
        "/portfolio-demo-check": FakeResponse(b"<html>CivicShield</html>","text/html"),
    }
    def opener(req, timeout=12):
        return cases[req.full_url.replace("http://127.0.0.1:5173", "")]
    with patch.object(smoke_compose,"urlopen",side_effect=opener):
        assert smoke_compose.check("http://127.0.0.1:5173")["result"]=="PASS"
        import pytest
        with pytest.raises(AssertionError,match="CI demo DB"):
            smoke_compose.check("http://127.0.0.1:5173",require_empty_db=True)
