"""Zero-dependency acceptance tests through the Docker Nginx frontend.

Runs from the HOST against the full Docker Compose stack. Makes only read-only
requests and an intentionally stale experimental risk request. No incident
submissions, outside data calls, or public safety decisions.
"""
from __future__ import annotations

import argparse
import json
import sys
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


def request(base: str, path: str, payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = Request(
        base.rstrip("/") + path,
        data=data, headers=headers, method="POST" if data is not None else "GET",
    )
    with urlopen(req, timeout=12) as response:
        body = response.read(1_000_000)
        return response.status, response.headers.get("Content-Type", ""), body


def check(base: str, require_empty_db: bool = False) -> dict:
    status, content_type, html = request(base, "/")
    assert status == 200 and "text/html" in content_type, "Nginx frontend not responding"
    assert b"CivicShield" in html and b"/assets/" in html, "Built React HTML not served"
    status, _, data = request(base, "/api/health")
    health = json.loads(data)
    assert status == 200 and health["mode"] == "research_demo"
    status, _, data = request(base, "/api/ready")
    ready = json.loads(data)
    assert status == 200 and ready["status"] == "ready"
    assert ready["official_emergency_service"] is False
    status, _, data = request(base, "/api/v1/alerts")
    alerts = json.loads(data)
    assert status == 200 and alerts["connection_state"] == "not_connected"
    assert alerts["official_alerts"] == []
    status, _, data = request(base, "/api/v1/demo/scenario")
    scenario = json.loads(data)
    assert status == 200 and len(scenario["samples"]) == 24
    assert scenario["is_synthetic"] and not scenario["official_data_connected"]
    assert scenario["database_reports_created"] == 0
    status, _, data = request(base, "/api/v1/analytics/summary")
    stats = json.loads(data)
    assert status == 200 and isinstance(stats["report_total"], int) and stats["report_total"] >= 0
    if require_empty_db:
        assert stats["report_total"] == 0, "Dedicated CI demo DB must start empty"
    status, _, data = request(base, "/api/v1/risk/estimate", {
        "city": "Test only", "rainfall_24h_mm": 0,
        "temperature_c": 25, "humidity_pct": 50, "forecast_age_hours": 7,
    })
    risk = json.loads(data)
    assert status == 200 and risk["risk_level"] == "unavailable"
    assert risk["is_official_warning"] is False
    # SPA route fallback shows the application shell rather than a 404.
    status, content_type, html = request(base, "/portfolio-demo-check")
    assert status == 200 and "text/html" in content_type and b"CivicShield" in html
    return {
        "result": "PASS",
        "checks": 8,
        "stack_components": ["PostgreSQL/PostGIS", "FastAPI", "Nginx/React"],
        "incident_database_modified": False,
        "external_warning_feeds_validated": False,
        "scientifically_validated_hazard_predictions": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://127.0.0.1:5173")
    parser.add_argument("--require-empty-db", action="store_true", help="Only for isolated disposable CI database")
    args = parser.parse_args()
    try:
        result = check(args.base, require_empty_db=args.require_empty_db)
    except (URLError, HTTPError, ValueError, AssertionError) as exc:
        print("Docker stack acceptance FAILED:", exc, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
