"""Geographic search must not leak reports or fabricate emergency capabilities."""
from __future__ import annotations
import pytest
from backend.app.geo_query import bbox, find_nearby
from backend.app.reviewer_identity import actor_reference
from backend.app.db import SessionLocal, Incident

REVIEWER = {"X-Responder-Key": "test-only-review-key"}

def sample(title, latitude, longitude):
    return {
        "title": title,
        "description": "An unverified fictional public road obstruction near the market.",
        "city": "Demo district",
        "latitude": latitude, "longitude": longitude,
    }

def test_antimeridian_bbox_includes_both_sides():
    lat_min, lat_max, ranges = bbox(0.0, 179.99, 30)
    assert lat_min < 0 < lat_max
    assert len(ranges) == 2
    assert any(w <= -179.99 <= e for w, e in ranges)
    assert any(w <= 179.99 <= e for w, e in ranges)

def test_polar_bbox_does_not_exclude_longitudes():
    lo, hi, ranges = bbox(89.9, 5.0, 40)
    assert hi == 90
    assert ranges == [(-180.0, 180.0)]

def test_portable_search_no_unrelated_reports(client, monkeypatch):
    monkeypatch.setenv("GEOSPATIAL_BACKEND", "portable")
    one = client.post("/api/v1/incidents", json=sample("Unverified obstruction Alpha", 17.38, 78.48))
    two = client.post("/api/v1/incidents", json=sample("Unverified obstruction Beta", 20.0, 78.48))
    assert one.status_code == 201 and two.status_code == 201
    r = client.get("/api/v1/incidents/nearby?latitude=17.38&longitude=78.48&radius_km=3",headers=REVIEWER)
    assert r.status_code == 200
    j = r.json()
    assert j["search_backend"] == "portable_bbox_haversine"
    assert j["possibly_incomplete"] is False
    assert [r["id"] for r in j["incidents"]] == [one.json()["id"]]
    assert "Unverified" in j["warning"]

def test_portable_search_antimeridian(client,monkeypatch):
    monkeypatch.setenv("GEOSPATIAL_BACKEND", "portable")
    r = client.post("/api/v1/incidents", json=sample("Port boundary sample record",0.0,-179.99))
    assert r.status_code == 201
    results = client.get("/api/v1/incidents/nearby?latitude=0&longitude=179.99&radius_km=10",headers=REVIEWER)
    assert results.status_code == 200
    assert any(v["id"]==r.json()["id"] for v in results.json()["incidents"])

def test_postgis_mode_refuses_sqlite(client, monkeypatch):
    monkeypatch.setenv("GEOSPATIAL_BACKEND","postgis")
    results = client.get("/api/v1/incidents/nearby?latitude=0&longitude=0",headers=REVIEWER)
    assert results.status_code == 503
    assert "unavailable" in results.json()["detail"]

def test_actor_reference_is_stable_without_storing_subject():
    claims = {"iss":"https://accounts.example","sub":"person-123"}
    ref = actor_reference(claims)
    assert ref.startswith("oidc_")
    assert "person" not in ref
    assert actor_reference(claims) == ref
    assert actor_reference({"iss":"https://accounts.other","sub":"person-123"}) != ref
    assert actor_reference({"role":"local_demo_reviewer"}) == "local_demo_shared_key"

def test_local_review_audit_is_explicitly_unattributed(client):
    r=client.post("/api/v1/incidents", json=sample("Demo reviewer record",17.3,78.3))
    assert r.status_code==201
    reviewed=client.patch("/api/v1/incidents/"+r.json()["id"]+"/review",
        json={"status":"needs_info","reviewer_note":"More detail required"},headers=REVIEWER)
    assert reviewed.status_code==200
    events=client.get("/api/v1/incidents/audit",headers=REVIEWER).json()["events"]
    assert events[0]["actor_ref"]=="local_demo_shared_key"

def test_geospatial_endpoint_requires_reviewer_role(client):
    url="/api/v1/incidents/nearby?latitude=17.3&longitude=78.3"
    assert client.get(url).status_code==403
    assert client.get(url,headers={"X-Responder-Key":"wrong"}).status_code==403
    assert client.get(url+"&radius_km=51",headers=REVIEWER).status_code==422
