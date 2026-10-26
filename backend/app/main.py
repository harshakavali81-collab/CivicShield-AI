"""Public safety research API — deliberately NOT an emergency alerting platform."""
from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
import hmac
import os
from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from backend.app.config import responder_key, submissions_enabled
from backend.app.db import Base, Incident, engine, get_db
from backend.app.schemas import AssistantQuestion, IncidentCreate, IncidentReview, RiskRequest
from civicshield.assistant.guidance import answer
from civicshield.incident_management.triage import (
    categorize, duplicate_fingerprint, priority_hint, redact_contact_info,
)
from civicshield.ingestion.sources import SOURCE_CATALOG
from civicshield.ml.predict import estimate_risk

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="CivicShield AI — Demonstration API",
    description="Experimental decision support ONLY. Not an official warning or dispatch system.",
    version="0.1.0",
    lifespan=lifespan,
)

def require_reviewer(x_responder_key: str | None = Header(default=None)):
    secret = responder_key()
    if not secret:
        raise HTTPException(status_code=503, detail="Responder review not configured")
    if not x_responder_key or not hmac.compare_digest(x_responder_key, secret):
        raise HTTPException(status_code=403, detail="Responder authentication required")
    return True

def public_incident(incident: Incident) -> dict:
    # Intentionally never publish reporter narrative, exact coordinates, or identifying data.
    return {
        "id": incident.id, "status": incident.status, "category": incident.category,
        "city": incident.city, "priority_hint": incident.priority_hint,
        "created_at": incident.created_at.isoformat(),
    }

def reviewer_incident(incident: Incident) -> dict:
    return {
        **public_incident(incident),
        "title": incident.title, "description": incident.description,
        "latitude": incident.latitude, "longitude": incident.longitude,
        "duplicate_of": incident.duplicate_of, "reviewer_note": incident.reviewer_note,
    }

@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok", "mode": "research_demo", "timestamp_utc": datetime.now(timezone.utc).isoformat()}

@app.get("/api/v1/sources", tags=["sources"])
def sources():
    return {"sources": SOURCE_CATALOG, "automated_alert_ingestion": False}

@app.get("/api/v1/alerts", tags=["sources"])
def alerts():
    return {
        "official_alerts": [], "connection_state": "not_connected",
        "message": "No live official alert feed is connected; an empty list does not mean there are no warnings.",
        "sources": SOURCE_CATALOG, "is_official_warning": False,
    }

@app.get("/api/v1/weather/sample", tags=["weather"])
def sample_weather():
    return {
        "city": "Hyderabad", "rainfall_24h_mm": 68.0,
        "temperature_c": 29.0, "humidity_pct": 85.0, "forecast_age_hours": 1.0,
        "source_type": "synthetic_demo", "not_live_weather": True,
        "notice": "These are invented sample values for UI testing, not observations or forecasts.",
    }

@app.post("/api/v1/risk/estimate", tags=["risk"])
def risk_estimate(request: RiskRequest):
    try:
        result = estimate_risk(
            request.rainfall_24h_mm, request.temperature_c,
            request.humidity_pct, request.forecast_age_hours,
        )
    except (ValueError, OSError, AttributeError) as exc:
        raise HTTPException(status_code=503, detail="Configured model unavailable; no estimate issued") from exc
    return {
        **result, "city": request.city, "source_type": "user_supplied",
        "is_official_warning": False,
        "warning": "EXPERIMENTAL ONLY — do not use to make evacuation or safety decisions.",
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
    }

@app.post("/api/v1/assistant/ask", tags=["assistant"])
def ask(request: AssistantQuestion):
    return answer(request.question, request.language)

@app.post("/api/v1/incidents", tags=["incidents"], status_code=201)
def create_incident(request: IncidentCreate, db: Session = Depends(get_db)):
    if not submissions_enabled():
        raise HTTPException(status_code=503, detail="Public submissions disabled until abuse/privacy safeguards are configured")
    title = redact_contact_info(request.title)
    description = redact_contact_info(request.description)
    city = redact_contact_info(request.city)
    category = categorize(title, description)
    fingerprint = duplicate_fingerprint(title, city, category)
    previous = db.scalar(select(Incident).where(Incident.dedup_hash == fingerprint).limit(1))
    report = Incident(
        title=title, description=description, city=city,
        latitude=request.latitude, longitude=request.longitude,
        language=request.language, category=category,
        priority_hint=priority_hint(title, description, category),
        duplicate_of=previous.id if previous else None,
        dedup_hash=fingerprint,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {
        **public_incident(report), "possible_duplicate": bool(previous),
        "message": "Report received for possible human review. NOT an emergency dispatch.",
    }

@app.get("/api/v1/incidents/review", tags=["responders"], dependencies=[Depends(require_reviewer)])
def review_queue(db: Session = Depends(get_db)):
    reports = db.scalars(select(Incident).order_by(Incident.created_at.desc()).limit(100)).all()
    return {"incidents": [reviewer_incident(r) for r in reports], "limit": 100}

@app.patch("/api/v1/incidents/{incident_id}/review", tags=["responders"], dependencies=[Depends(require_reviewer)])
def review_report(incident_id: str, request: IncidentReview, db: Session = Depends(get_db)):
    report = db.get(Incident, incident_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = request.status
    report.reviewer_note = redact_contact_info(request.reviewer_note)
    db.commit()
    db.refresh(report)
    return reviewer_incident(report)

@app.get("/api/v1/analytics/summary", tags=["analytics"])
def summary(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count()).select_from(Incident)) or 0
    grouped = db.execute(select(Incident.status, func.count()).group_by(Incident.status)).all()
    categories = db.execute(select(Incident.category, func.count()).group_by(Incident.category)).all()
    return {
        "report_total": total,
        "by_status": {k: v for k, v in grouped},
        "by_category": {k: v for k, v in categories},
        "verified_alert_count": None,
        "live_hazard_feed_connected": False,
        "source_type": "locally_submitted_reports",
        "note": "Counts reflect only locally stored demo reports, not real-world disaster incidence.",
    }

@app.get("/api/v1/analytics/trends", tags=["analytics"])
def trends():
    today = datetime.now(timezone.utc).date()
    return {
        "data": [
            {"date": (today - timedelta(days=6-i)).isoformat(), "reports": n}
            for i, n in enumerate((2, 3, 2, 5, 4, 6, 3))
        ],
        "source_type": "synthetic_demo", "not_real_events": True,
    }
