"""Runtime configuration. Deploy with an external secret manager in production."""
from __future__ import annotations
import os

def database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///./civicshield.db")
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url

def submissions_enabled() -> bool:
    return os.getenv("INCIDENT_SUBMISSIONS_ENABLED", "false").lower() == "true"

def responder_key() -> str:
    return os.getenv("RESPONDER_API_KEY", "")
