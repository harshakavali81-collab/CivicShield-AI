"""Runtime configuration. Deploy with an external secret manager in production."""
from __future__ import annotations
import os

def database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./civicshield.db")

def submissions_enabled() -> bool:
    return os.getenv("INCIDENT_SUBMISSIONS_ENABLED", "false").lower() == "true"

def responder_key() -> str:
    return os.getenv("RESPONDER_API_KEY", "")
