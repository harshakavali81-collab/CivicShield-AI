"""Disposable CI-only smoke test for indexed PostGIS queries.

Prerequisite: DATABASE_URL must target a fresh dedicated PostgreSQL/PostGIS test
database; run Alembic migrations first. Never run against a live production DB.
"""
from __future__ import annotations
import os
from pathlib import Path
import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.db import engine, Incident
from backend.app.geo_query import find_nearby

def smoke():
    if os.getenv("CI_POSTGIS_TEST") != "true" or engine.dialect.name != "postgresql":
        raise RuntimeError("Only run with CI_POSTGIS_TEST=true against an isolated PostgreSQL database")
    index_sql = Path("backend/migrations/postgis_indexes.sql").read_text("utf-8")
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        connection.execute(text("""
        CREATE INDEX IF NOT EXISTS ix_incidents_geography_gist
        ON incidents USING GIST (
          (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography)
        ) WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        """))
        assert connection.scalar(text("SELECT PostGIS_Version()"))
        assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "20261028_0002"
    os.environ["GEOSPATIAL_BACKEND"] = "postgis"
    prefix = "CI ONLY " + uuid.uuid4().hex[:10]
    records = [
        Incident(title=prefix+" close", description="Fictional test only", category="other",
                 city="CI sandbox", latitude=17.38, longitude=78.48,
                 language="en", priority_hint="normal", dedup_hash=uuid.uuid4().hex),
        Incident(title=prefix+" far", description="Fictional test only", category="other",
                 city="CI sandbox", latitude=30.0, longitude=78.48,
                 language="en", priority_hint="normal", dedup_hash=uuid.uuid4().hex),
        Incident(title=prefix+" antimeridian", description="Fictional test only",category="other",
                 city="CI sandbox", latitude=0.0, longitude=-179.99,
                 language="en", priority_hint="normal", dedup_hash=uuid.uuid4().hex),
    ]
    with Session(engine) as session:
        ids = []
        try:
            session.add_all(records)
            session.commit()
            ids = [r.id for r in records]
            near = find_nearby(session,17.38,78.48,5)
            assert near.backend == "postgis_geography"
            assert ids[0] in [v.id for v, _ in near.matches]
            assert ids[1] not in [v.id for v, _ in near.matches]
            cross = find_nearby(session,0.0,179.99,10)
            assert ids[2] in [v.id for v, _ in cross.matches]
            print("PostGIS index + distance search + antimeridian smoke checks passed")
        finally:
            session.rollback()
            for r in records:
                if r.id is not None:
                    obj = session.get(Incident,r.id)
                    if obj is not None:
                        session.delete(obj)
            session.commit()

if __name__ == "__main__":
    smoke()
