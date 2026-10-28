"""The portfolio scenario must be deterministic, offline and incapable of issuing alerts."""
from __future__ import annotations

from civicshield.demo.scenarios import build_scenario, RAIN_MM, REPORT_COUNTS

def test_scenario_is_reproducible_and_fully_labeled():
    a, b = build_scenario(), build_scenario()
    assert a == b
    assert a["mode"] == "deterministic_static_simulation"
    assert a["source_type"] == "synthetic_portfolio_exercise"
    assert a["is_synthetic"] is True
    assert a["is_official_warning"] is False
    assert a["official_data_connected"] is False
    assert a["real_hazard_predictions"] is False
    assert a["external_services_called"] is False
    assert a["database_reports_created"] == 0
    assert a["metadata"]["scientific_validation"] is False

def test_synthetic_chart_integrity():
    s = build_scenario()
    assert len(s["samples"]) == 24
    assert [row["hour"] for row in s["samples"]] == list(range(24))
    assert all(row["is_synthetic"] is True for row in s["samples"])
    assert s["summary"]["invented_report_total"] == sum(REPORT_COUNTS)
    assert s["summary"]["invented_precipitation_total_mm"] == sum(RAIN_MM)
    assert s["summary"]["max_hourly_precipitation_mm"] == max(RAIN_MM)
    assert len({row["timestamp_utc"] for row in s["samples"]}) == 24
    assert all(row["invented_report_count"] >= 0 for row in s["samples"])

def test_scenario_chapters_cannot_contain_an_official_instruction():
    s = build_scenario()
    assert len(s["chapters"]) == 4
    assert all(chapter["official_advisory"] is False for chapter in s["chapters"])
    assert all(chapter["id"] and chapter["operator_takeaway"] for chapter in s["chapters"])
    assert "FICTIONAL" in s["warning"]

def test_scenario_endpoint_returns_no_sensitive_or_government_data(client):
    before = client.get("/api/v1/analytics/summary").json()["report_total"]
    response = client.get("/api/v1/demo/scenario")
    assert response.status_code == 200
    assert response.json() == build_scenario()
    after = client.get("/api/v1/analytics/summary").json()["report_total"]
    assert before == after
    assert response.json()["database_reports_created"] == 0
    assert response.headers["cache-control"] == "no-store"
