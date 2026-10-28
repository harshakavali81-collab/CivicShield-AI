"""Differentiate infrastructure health from public-safety reliability."""
import pytest
from sqlalchemy import text
from backend.app.db import SessionLocal

def test_readiness_is_not_emergency_approval(client):
    health = client.get("/api/health")
    ready = client.get("/api/ready")
    assert health.status_code == 200
    assert ready.status_code == 200
    assert ready.json()["database"] == "connected"
    assert ready.json()["official_emergency_service"] is False
    assert "hazard" in ready.json()["notice"].lower()

def test_wrong_geospatial_backend_reports_unready(client, monkeypatch):
    monkeypatch.setenv("GEOSPATIAL_BACKEND", "postgis")
    response = client.get("/api/ready")
    assert response.status_code == 503
    assert "schema not ready" in response.json()["detail"]
