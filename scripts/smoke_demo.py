"""Read-only end-to-end smoke checks against a running CivicShield demo API.

Usage:
  python -m scripts.smoke_demo --url http://localhost:8000
No government feeds, reviewer keys, private reports or paid services required.
"""
from __future__ import annotations
import argparse
import httpx

RISK_OLD = {
    "city": "Test locality", "rainfall_24h_mm": 68,
    "temperature_c": 29, "humidity_pct": 80, "forecast_age_hours": 10,
}

def smoke(client) -> dict:
    health = client.get("/api/health")
    health.raise_for_status()
    assert health.json()["mode"] == "research_demo"

    ready = client.get("/api/ready")
    ready.raise_for_status()
    assert ready.json()["official_emergency_service"] is False

    alerts = client.get("/api/v1/alerts")
    alerts.raise_for_status()
    assert alerts.json()["connection_state"] == "not_connected"
    assert alerts.json()["official_alerts"] == []

    sources = client.get("/api/v1/official/integration-status")
    sources.raise_for_status()
    assert sources.json()["cwc"]["api_connected"] is False

    sample = client.get("/api/v1/weather/sample")
    sample.raise_for_status()
    assert sample.json()["source_type"] == "synthetic_demo"

    risk = client.post("/api/v1/risk/estimate", json=RISK_OLD)
    risk.raise_for_status()
    assert risk.json()["risk_level"] == "unavailable"
    assert risk.json()["is_official_warning"] is False

    library = client.get("/api/v1/assistant/knowledge", params={"q": "flood"})
    library.raise_for_status()
    assert library.json()["live_retrieval"] is False

    return {
        "status": "software_demo_smoke_passed",
        "checks": 7,
        "live_government_feed_verified": False,
        "validated_emergency_prediction": False,
        "reports_submitted": 0,
        "note": "Passing smoke tests proves only these local endpoint behaviors.",
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8000")
    args = parser.parse_args()
    with httpx.Client(base_url=args.url,timeout=8,follow_redirects=False,trust_env=False) as client:
        result = smoke(client)
    for key, value in result.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
