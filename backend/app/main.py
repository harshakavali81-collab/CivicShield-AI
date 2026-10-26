"""Public safety research API — deliberately NOT an emergency alerting platform."""
from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
import hmac
import os
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session
from backend.app.config import responder_key, submissions_enabled
from backend.app.db import Base, Incident, ReviewAudit, engine, get_db
from backend.app.schemas import AssistantQuestion, IncidentCreate, IncidentReview, RiskRequest
from civicshield.assistant.guidance import answer
from civicshield.incident_management.triage import (
    categorize, duplicate_fingerprint, priority_hint, redact_contact_info,
)
from civicshield.ingestion.sources import SOURCE_CATALOG
from civicshield.ml.predict import estimate_risk
from civicshield.ingestion.open_meteo import fetch_weather
from civicshield.assistant.retrieval import search_docs
from civicshield.incident_management.geospatial import haversine_km
from backend.app.security import require_reporter_key, rate_limit, security_headers
from backend.app.oidc import oidc_enabled, require_oidc_reviewer, validate_production_configuration
from civicshield.ingestion.imd_official import enabled as imd_enabled, fetch_district_warning
from civicshield.ingestion.cwc_official import integration_status

@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_production_configuration()
    if os.getenv("APP_ENV", "local") != "production":
        Base.metadata.create_all(bind=engine)
    else:
        # Production schema must already have completed reviewed Alembic migrations.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    yield

app = FastAPI(
    title="CivicShield AI — Demonstration API",
    description="Experimental decision support ONLY. Not an official warning or dispatch system.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def apply_security_headers(request: Request, call_next):
    return security_headers(await call_next(request))

def require_reviewer(request: Request, x_responder_key: str | None = Header(default=None)):
    if oidc_enabled():
        return require_oidc_reviewer(request)
    if os.getenv("APP_ENV", "local") == "production":
        raise HTTPException(status_code=503, detail="Demo authentication not permitted in production")
    secret = responder_key()
    if not secret:
        raise HTTPException(status_code=503, detail="Responder review not configured")
    if not x_responder_key or not hmac.compare_digest(x_responder_key, secret):
        raise HTTPException(status_code=403, detail="Responder authentication required")
    return {"role": "local_demo_reviewer"}

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


@app.get("/api/v1/official/integration-status", tags=["sources"])
def official_integration_status():
    return {
        "imd": {
            "enabled": imd_enabled(),
            "api_reference": "https://api.imd.gov.in/public/api_reference.html",
            "note": "Enabled does not prove access, freshness or legal authorization.",
        },
        "cwc": integration_status(),
        "warning": "Disconnection or failed requests never imply an area is safe.",
    }

@app.get("/api/v1/official/imd/district-warning", tags=["sources"])
async def imd_district_warning(
    request: Request,
    district_id: int = Query(ge=1, le=999999),
):
    if not imd_enabled():
        raise HTTPException(status_code=503, detail="IMD API access not configured")
    rate_limit(request, "imd_official", limit=15, window_seconds=3600)
    try:
        return await fetch_district_warning(district_id)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Official district bulletin could not be authenticated, parsed or verified as fresh; consult IMD directly",
        ) from exc

@app.get("/api/v1/weather/sample", tags=["weather"])
def sample_weather():
    return {
        "city": "Hyderabad", "rainfall_24h_mm": 68.0,
        "temperature_c": 29.0, "humidity_pct": 85.0, "forecast_age_hours": 1.0,
        "source_type": "synthetic_demo", "not_live_weather": True,
        "notice": "These are invented sample values for UI testing, not observations or forecasts.",
    }

@app.get("/api/v1/weather/live", tags=["weather"])
async def live_weather(
    request: Request,
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
):
    if os.getenv("OPEN_METEO_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=503, detail="Modeled weather feed disabled by operator")
    rate_limit(request, "live_weather", limit=20, window_seconds=3600)
    try:
        return await fetch_weather(latitude, longitude)
    except Exception as exc:
        # Includes upstream service outages and invalid/insufficient data.
        # Fail closed: never substitute a demo figure as live weather.
        raise HTTPException(status_code=503, detail="Modeled weather unavailable; consult official sources") from exc

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

@app.get("/api/v1/assistant/knowledge", tags=["assistant"])
def knowledge_search(request: Request, q: str = Query(min_length=2, max_length=200)):
    rate_limit(request, "knowledge", limit=120, window_seconds=3600)
    return {
        "items": search_docs(q), "corpus_size": 5, "live_retrieval": False,
        "source_type": "manual_curated_summaries",
        "warning": "Educational summaries only, not latest safety bulletins or official notices.",
    }

@app.post("/api/v1/incidents", tags=["incidents"], status_code=201)
def create_incident(request: IncidentCreate, http_request: Request, db: Session = Depends(get_db)):
    if not submissions_enabled():
        raise HTTPException(status_code=503, detail="Public submissions disabled until abuse/privacy safeguards are configured")
    require_reporter_key(http_request)
    rate_limit(http_request, "report", limit=30, window_seconds=3600)
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
    previous = report.status
    report.status = request.status
    report.reviewer_note = redact_contact_info(request.reviewer_note)
    db.add(ReviewAudit(
        incident_id=incident_id, previous_status=previous, new_status=request.status,
        reviewer_note=report.reviewer_note,
    ))
    db.commit()
    db.refresh(report)
    return reviewer_incident(report)

@app.get("/api/v1/incidents/nearby", tags=["responders"], dependencies=[Depends(require_reviewer)])
def nearby_incidents(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=10, gt=0, le=50),
    db: Session = Depends(get_db),
):
    # Bounded demo query; use ST_DWithin with a verified PostGIS schema at scale.
    candidates = db.scalars(
        select(Incident).where(
            Incident.latitude.is_not(None), Incident.longitude.is_not(None),
        ).order_by(Incident.created_at.desc()).limit(5000)
    ).all()
    matches = []
    for incident in candidates:
        distance = haversine_km(latitude, longitude, incident.latitude, incident.longitude)
        if distance <= radius_km:
            matches.append({**reviewer_incident(incident), "distance_km": round(distance, 2)})
    matches.sort(key=lambda item: item["distance_km"])
    return {
        "incidents": matches[:100],
        "radius_km": radius_km,
        "scanned_limit": 5000,
        "total_matches_in_scan": len(matches),
        "warning": "Unverified citizen reports only. This bounded scan is not authoritative or exhaustive.",
    }

@app.get("/api/v1/incidents/audit", tags=["responders"], dependencies=[Depends(require_reviewer)])
def review_audit(db: Session = Depends(get_db)):
    events = db.scalars(select(ReviewAudit).order_by(ReviewAudit.changed_at.desc()).limit(100)).all()
    return {"events": [
        {
            "id": e.id, "incident_id": e.incident_id,
            "previous_status": e.previous_status, "new_status": e.new_status,
            "changed_at": e.changed_at.isoformat(),
        }
        for e in events
    ], "note": "Local demo audit; not verified actor attribution."}

@app.get("/api/v1/ops/status", tags=["operations"], dependencies=[Depends(require_reviewer)])
def ops_status(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "database": "reachable",
        "modeled_weather_enabled": os.getenv("OPEN_METEO_ENABLED", "false").lower() == "true",
        "official_alert_feed_connected": False,
        "reporter_access_key_configured": bool(os.getenv("REPORTER_API_KEY")),
        "reviewer_access_key_configured": bool(responder_key()),
        "incident_submissions_enabled": submissions_enabled(),
        "notice": "Does not measure actual production health or safety coverage.",
    }

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
def trends(db: Session = Depends(get_db)):
    # Accurate counts of locally submitted demo reports, not nationwide events.
    today = datetime.now(timezone.utc).date()
    days = [(today - timedelta(days=6-i)) for i in range(7)]
    totals = {d.isoformat(): 0 for d in days}
    since = datetime.combine(days[0], datetime.min.time(), tzinfo=timezone.utc)
    dates = db.scalars(select(Incident.created_at).where(Incident.created_at >= since)).all()
    for created_at in dates:
        # SQLite may round-trip tz-naive UTC values; normalize explicitly.
        timestamp = created_at if created_at.tzinfo else created_at.replace(tzinfo=timezone.utc)
        key = timestamp.astimezone(timezone.utc).date().isoformat()
        if key in totals:
            totals[key] += 1
    return {
        "data": [{"date": date, "reports": totals[date]} for date in totals],
        "source_type": "locally_submitted_demo_reports",
        "not_real_events": True,
        "note": "Actual locally stored report counts; not validated disaster occurrences.",
    }
