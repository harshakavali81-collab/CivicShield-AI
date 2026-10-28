"""Deterministic educational story data: no API calls, DB writes, or true events.

A case study should be replayable offline and distinguish fictional samples
from source-backed records and independently validated models.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

SCENARIO_ID = "fictional-monsoon-exercise"
START = datetime(2026, 8, 11, 0, 0, tzinfo=timezone.utc)
RAIN_MM = (0, 0, 0, 1, 1, 2, 4, 7, 9, 10, 12, 15, 12, 9, 7, 4, 3, 1, 1, 0, 0, 0, 0, 0)
REPORT_COUNTS = (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 2, 4, 2, 2, 1, 1, 0, 0, 0, 0, 0)

def build_scenario() -> dict:
    samples = [
        {
            "hour": hour,
            "timestamp_utc": (START + timedelta(hours=hour)).isoformat(),
            "invented_hourly_precipitation_mm": RAIN_MM[hour],
            "invented_report_count": REPORT_COUNTS[hour],
            "is_synthetic": True,
        }
        for hour in range(len(RAIN_MM))
    ]
    return {
        "id": SCENARIO_ID,
        "title": "Fictional Monsoon Readiness Exercise",
        "subtitle": "Offline, fully invented end-to-end case study",
        "mode": "deterministic_static_simulation",
        "source_type": "synthetic_portfolio_exercise",
        "is_synthetic": True,
        "is_official_warning": False,
        "official_data_connected": False,
        "real_hazard_predictions": False,
        "external_services_called": False,
        "database_reports_created": 0,
        "city": "Fictional City — not a real incident location",
        "timezone": "UTC",
        "metadata": {
            "version": 1,
            "generator": "src/civicshield/demo/scenarios.py",
            "license": "Repository MIT License",
            "observational_data": False,
            "scientific_validation": False,
        },
        "summary": {
            "hours": len(samples),
            "invented_precipitation_total_mm": sum(RAIN_MM),
            "invented_report_total": sum(REPORT_COUNTS),
            "max_hourly_precipitation_mm": max(RAIN_MM),
            "note": "These quantities are fabricated to exercise charts and software workflows.",
        },
        "chapters": [
            {
                "id": "source",
                "title": "1. Keep original sources distinct",
                "hour": 0,
                "explanation": "The exercise begins with invented rainfall samples. Official IMD/CWC warnings remain disconnected unless properly authorized and verified.",
                "action_type": "provenance_check",
                "operator_takeaway": "A failed official feed never means no warning.",
                "official_advisory": False,
            },
            {
                "id": "validation",
                "title": "2. Reject stale inputs",
                "hour": 9,
                "explanation": "Demonstrate how the risk endpoint refuses user-supplied stale conditions. The rainfall series here is not a forecast.",
                "action_type": "freshness_gate",
                "operator_takeaway": "Unreliable or missing inputs should result in unavailable, not an all-clear.",
                "official_advisory": False,
            },
            {
                "id": "review",
                "title": "3. Separate reported events from confirmed events",
                "hour": 14,
                "explanation": "Fictional submitted report counts illustrate an audit workflow. A priority hint does not verify the narrative or trigger emergency services.",
                "action_type": "human_moderation",
                "operator_takeaway": "Human review is required; simulated reports are never inserted into the real incident table.",
                "official_advisory": False,
            },
            {
                "id": "evaluation",
                "title": "4. Evaluate errors before any real use",
                "hour": 23,
                "explanation": "The portfolio provides geographical and temporal holdout evaluation code for permitted labeled data. No genuine outcome labels are bundled.",
                "action_type": "model_governance",
                "operator_takeaway": "Charts of fabricated data are NOT evidence of flood prediction accuracy.",
                "official_advisory": False,
            },
        ],
        "samples": samples,
        "warning": (
            "FICTIONAL TRAINING EXERCISE ONLY. All numbers and story events are invented. "
            "No government warnings, verified reports, rescue or evacuation recommendations."
        ),
    }
