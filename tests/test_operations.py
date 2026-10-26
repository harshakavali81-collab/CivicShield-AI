"""Migration-era operations and reviewer-only location search (no live vendor calls)."""
import json
import sqlite3
from datetime import datetime, timezone
from civicshield.incident_management.geospatial import haversine_km
from scripts.backup_sqlite import backup
from scripts.collect_weather import save_jsonl
from scripts.check_data_quality import audit
from pathlib import Path
import pandas as pd

def test_geographic_distance_properties():
    assert haversine_km(17.38, 78.48, 17.38, 78.48) == 0
    assert 95 < haversine_km(17.38, 78.48, 18.38, 78.48) < 125
    assert abs(haversine_km(0, 0, 0, 179) - haversine_km(0, 179, 0, 0)) < 0.01

def test_nearby_endpoint_private_and_sorted(client):
    assert client.get("/api/v1/incidents/nearby?latitude=17.38&longitude=78.48").status_code == 403
    payload = {
        "title": "Flooding near public square",
        "description": "Deep water covers part of the main street.",
        "city": "Hyderabad",
        "latitude": 17.38, "longitude": 78.48,
    }
    response = client.post("/api/v1/incidents", json=payload)
    assert response.status_code == 201
    rid = response.json()["id"]
    response = client.get(
        "/api/v1/incidents/nearby?latitude=17.38&longitude=78.48&radius_km=1",
        headers={"X-Responder-Key": "test-only-review-key"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["incidents"]) == 1
    assert data["incidents"][0]["distance_km"] == 0
    assert data["incidents"][0]["id"] == rid
    assert client.get("/api/v1/incidents/nearby?latitude=17.38&longitude=78.48&radius_km=100", headers={"X-Responder-Key":"test-only-review-key"}).status_code == 422

def test_sqlite_backup_is_valid_snapshot(client, tmp_path):
    assert client.get("/api/health").status_code == 200
    path = backup(tmp_path / "snapshot.db")
    assert path.is_file()
    with sqlite3.connect(path) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "incidents" in tables and "review_audit" in tables

def test_collector_writes_private_jsonl_without_network(tmp_path):
    dest = tmp_path / "data" / "raw" / "provider.jsonl"
    record = {"source_type": "third_party_modeled_weather", "is_official_warning": False}
    save_jsonl(record, dest)
    save_jsonl(record, dest)
    content = dest.read_text(encoding="utf-8").splitlines()
    assert len(content) == 2
    assert json.loads(content[0]) == record

def test_quality_report_does_not_claim_validated_labels(tmp_path):
    path = tmp_path / "weather.csv"
    pd.DataFrame([{
        "observed_at": "2025-01-01T00:00:00+00:00",
        "rainfall_24h_mm": 15, "temperature_c": 27,
        "humidity_pct": 73, "risk_label": 0,
    }, {
        "observed_at": "invalid", "rainfall_24h_mm": None, "temperature_c": 30,
        "humidity_pct": 74, "risk_label": 1,
    }]).to_csv(path, index=False)
    result = audit(str(path))
    assert result["invalid_timestamp_count"] == 1
    assert result["feature_missing_counts"]["rainfall_24h_mm"] == 1
    assert "do not" in result["caveat"].lower()
