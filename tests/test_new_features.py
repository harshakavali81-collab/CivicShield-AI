"""Offline tests for modeled source integration, provenance, role gates and audit logging."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
import asyncio
import pytest

from civicshield.assistant.retrieval import search_docs
from civicshield.ingestion.open_meteo import normalize, fetch_weather, _cache
from civicshield.monitoring.drift import distribution_shift
from backend.app.security import _times

def modeled_payload(hours=25, age=0):
    anchor = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) - timedelta(hours=age)
    times = [(anchor - timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M") for i in range(hours)]
    return {
        "current": {
            "time": anchor.strftime("%Y-%m-%dT%H:%M"),
            "temperature_2m": 27.1,
            "relative_humidity_2m": 80,
        },
        "hourly": {"time": times, "precipitation": [1.5] * len(times)},
    }

def test_provider_response_fresh_and_precipitation_sum():
    weather = normalize(modeled_payload(), 17.38, 78.48)
    assert weather["source_type"] == "third_party_modeled_weather"
    assert weather["is_official_warning"] is False
    assert weather["is_ground_observation"] is False
    assert weather["modeled_precipitation_24h_mm"] == 36
    assert weather["license_url"].endswith("/4.0/")

def test_provider_response_fail_closed():
    with pytest.raises((ValueError, KeyError)):
        normalize({"current": {"time": "2026-01-01"}, "hourly": {}}, 17, 78)
    with pytest.raises(ValueError, match="Insufficient"):
        normalize(modeled_payload(hours=3), 17, 78)
    with pytest.raises(ValueError, match="timestamp"):
        normalize(modeled_payload(age=48), 17, 78)

def test_provider_client_is_cached_and_coordinates_coarsened(monkeypatch):
    from civicshield.ingestion import open_meteo
    _cache.clear()
    hits = []
    class Response:
        def raise_for_status(self):
            pass
        def json(self):
            return modeled_payload()
    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            pass
        async def get(self, url, params):
            hits.append((url, params))
            return Response()
    monkeypatch.setattr(open_meteo.httpx, "AsyncClient", FakeClient)
    one = asyncio.run(fetch_weather(17.384, 78.484))
    two = asyncio.run(fetch_weather(17.381, 78.481))
    assert one["cache_hit"] is False
    assert two["cache_hit"] is True
    assert len(hits) == 1
    assert hits[0][1]["latitude"] == 17.38
    _cache.clear()

def test_disabled_weather_endpoint_has_no_synthetic_fallback(client, monkeypatch):
    monkeypatch.setenv("OPEN_METEO_ENABLED", "false")
    response = client.get("/api/v1/weather/live?latitude=17.38&longitude=78.48")
    assert response.status_code == 503

def test_live_weather_endpoint_mocked_provider(client, monkeypatch):
    monkeypatch.setenv("OPEN_METEO_ENABLED", "true")
    import backend.app.main as main_module
    async def fake_feed(lat, long):
        return normalize(modeled_payload(), round(lat, 2), round(long, 2))
    monkeypatch.setattr(main_module, "fetch_weather", fake_feed)
    response = client.get("/api/v1/weather/live?latitude=17.38&longitude=78.48")
    assert response.status_code == 200
    assert response.json()["is_official_warning"] is False
    assert response.json()["modeled_precipitation_24h_mm"] == 36
    assert client.get("/api/v1/weather/live?latitude=177&longitude=78").status_code == 422

def test_knowledge_search_has_sourced_docs_and_no_fabricated_alert(client):
    result = client.get("/api/v1/assistant/knowledge?q=flood").json()
    assert result["live_retrieval"] is False
    assert any(x["topic"] == "flood" for x in result["items"])
    assert all(x["source_url"].startswith("https://") for x in result["items"])
    assert search_docs("somethingunrelatedxyz") == []

def test_security_headers(client):
    response = client.get("/api/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-frame-options"] == "DENY"

def test_submission_reporter_key_if_configured(client, monkeypatch):
    monkeypatch.setenv("INCIDENT_SUBMISSIONS_ENABLED", "true")
    monkeypatch.setenv("REPORTER_API_KEY", "test-reporter-key")
    payload = {
        "title": "Blocked road near bridge",
        "description": "A large object blocks the road near the bridge.",
        "city": "Hyderabad",
    }
    assert client.post("/api/v1/incidents", json=payload).status_code == 403
    response = client.post("/api/v1/incidents", json=payload, headers={"X-Reporter-Key": "test-reporter-key"})
    assert response.status_code == 201

def test_audit_endpoint_requires_reviewer_and_records_changes(client):
    payload = {
        "title": "Flooded public street",
        "description": "Water has covered the road near the market entrance.",
        "city": "Hyderabad",
    }
    monkey = client.post("/api/v1/incidents", json=payload)
    assert monkey.status_code == 201
    incident_id = monkey.json()["id"]
    assert client.get("/api/v1/incidents/audit").status_code == 403
    headers = {"X-Responder-Key": "test-only-review-key"}
    result = client.patch(f"/api/v1/incidents/{incident_id}/review", headers=headers, json={
        "status": "needs_info", "reviewer_note": "Need more context"
    })
    assert result.status_code == 200
    events = client.get("/api/v1/incidents/audit", headers=headers).json()["events"]
    assert len(events) == 1
    assert events[0]["previous_status"] == "pending"
    assert events[0]["new_status"] == "needs_info"
    assert events[0]["incident_id"] == incident_id
    assert client.get("/api/v1/ops/status").status_code == 403
    ops = client.get("/api/v1/ops/status", headers=headers).json()
    assert ops["database"] == "reachable"
    assert ops["official_alert_feed_connected"] is False

def test_trend_counts_are_real_local_entries(client):
    before = client.get("/api/v1/analytics/trends").json()
    assert sum(row["reports"] for row in before["data"]) == 0
    body = {
        "title": "Fallen tree on road",
        "description": "Public road blocked by large fallen tree.",
        "city": "Hyderabad",
    }
    assert client.post("/api/v1/incidents", json=body).status_code == 201
    after = client.get("/api/v1/analytics/trends").json()
    assert after["data"][-1]["reports"] == 1
    assert after["source_type"] == "locally_submitted_demo_reports"

def test_shift_heuristic_requires_samples():
    assert distribution_shift([1] * 10, [2] * 10)["status"] == "insufficient_data"
    result = distribution_shift(list(range(100)), list(range(100, 200)))
    assert result["status"] == "review_recommended"
    assert result["drift_score"] > 1

def test_retention_purges_review_audit_with_report(client):
    from backend.app.db import Incident, ReviewAudit, SessionLocal
    from scripts.purge_incidents import purge
    from sqlalchemy import select, func
    original = client.post("/api/v1/incidents", json={
        "title": "Flood across main road",
        "description": "Water is covering several road lanes.",
        "city": "Hyderabad",
    })
    assert original.status_code == 201
    rid = original.json()["id"]
    headers = {"X-Responder-Key": "test-only-review-key"}
    assert client.patch(f"/api/v1/incidents/{rid}/review", headers=headers, json={
        "status": "needs_info", "reviewer_note": "Request more context"
    }).status_code == 200
    with SessionLocal() as session:
        report = session.get(Incident, rid)
        report.created_at = datetime.now(timezone.utc) - timedelta(days=45)
        session.commit()
    assert purge(30, confirm=False) == 1
    with SessionLocal() as session:
        assert session.get(Incident, rid) is not None
    assert purge(30, confirm=True) == 1
    with SessionLocal() as session:
        assert session.get(Incident, rid) is None
        assert session.scalar(select(func.count()).select_from(ReviewAudit)) == 0
