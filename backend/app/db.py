"""SQLAlchemy persistence with SQLite locally and PostgreSQL in Compose."""
from __future__ import annotations
import os
import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from .config import database_url

url = database_url()
engine = create_engine(
    url, pool_pre_ping=True,
    connect_args={"check_same_thread": False} if url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    language: Mapped[str] = mapped_column(String(5), default="en")
    priority_hint: Mapped[str] = mapped_column(String(16), default="normal")
    duplicate_of: Mapped[str | None] = mapped_column(String(36), nullable=True)
    dedup_hash: Mapped[str] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    reviewer_note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

class ReviewAudit(Base):
    """Local reviewer audit. No identity proof beyond configured shared demo key."""
    __tablename__ = "review_audit"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id: Mapped[str] = mapped_column(String(36), index=True)
    actor_ref: Mapped[str] = mapped_column(String(64), default="local_demo_shared_key", nullable=False)
    previous_status: Mapped[str] = mapped_column(String(20))
    new_status: Mapped[str] = mapped_column(String(20))
    reviewer_note: Mapped[str] = mapped_column(Text, default="")
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

def get_db():
    with SessionLocal() as session:
        yield session
