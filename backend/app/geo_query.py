"""Bounded local and index-backed PostGIS search for *unverified* citizen reports.

Never provides navigation, rescue dispatch, or an authoritative hazard map.
PostGIS requires explicit GEOSPATIAL_BACKEND=postgis and separately installed
extension/index; otherwise a portable bbox + haversine search is used.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import os
from sqlalchemy import and_, or_, select, text
from sqlalchemy.orm import Session

from backend.app.db import Incident
from civicshield.incident_management.geospatial import haversine_km

MAX_SCAN = 5000
MAX_RETURN = 100
KM_LAT_DEGREE = 111.195

@dataclass
class GeoSearch:
    matches: list[tuple[Incident, float]]
    backend: str
    possibly_incomplete: bool
    scanned_limit: int

def bbox(latitude: float, longitude: float, radius_km: float):
    """Latitude bounds and 1 or 2 longitude ranges, supporting antimeridian/poles."""
    delta_lat = radius_km / KM_LAT_DEGREE
    min_lat = max(-90.0, latitude - delta_lat)
    max_lat = min(90.0, latitude + delta_lat)
    if min_lat <= -90 or max_lat >= 90:
        return min_lat, max_lat, [(-180.0, 180.0)]
    cos_lat = math.cos(math.radians(max(abs(min_lat), abs(max_lat))))
    lon_delta = min(180.0, radius_km / (KM_LAT_DEGREE * max(cos_lat, 1e-9)))
    if lon_delta >= 180:
        return min_lat, max_lat, [(-180.0, 180.0)]
    west, east = longitude - lon_delta, longitude + lon_delta
    if west < -180:
        return min_lat, max_lat, [(west + 360, 180.0), (-180.0, east)]
    if east > 180:
        return min_lat, max_lat, [(west, 180.0), (-180.0, east - 360)]
    return min_lat, max_lat, [(west, east)]

def find_nearby(db: Session, latitude: float, longitude: float, radius_km: float) -> GeoSearch:
    backend = os.getenv("GEOSPATIAL_BACKEND", "portable").strip().lower()
    if backend == "postgis":
        if db.get_bind().dialect.name != "postgresql":
            raise ValueError("PostGIS backend requires PostgreSQL and the installed PostGIS extension")
        # This exact geography expression is matched by ix_incidents_geography_gist.
        distance = """ST_Distance(
          ST_SetSRID(ST_MakePoint(longitude, latitude),4326)::geography,
          ST_SetSRID(ST_MakePoint(:longitude,:latitude),4326)::geography)"""
        query = text(f"""
          SELECT id, {distance} AS distance_m
          FROM incidents
          WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            AND ST_DWithin(
              ST_SetSRID(ST_MakePoint(longitude, latitude),4326)::geography,
              ST_SetSRID(ST_MakePoint(:longitude,:latitude),4326)::geography,
              :meters)
          ORDER BY distance_m ASC, id ASC
          LIMIT :limit
        """)
        rows = db.execute(query, {
            "latitude": latitude, "longitude": longitude,
            "meters": radius_km * 1000, "limit": MAX_RETURN + 1,
        }).all()
        truncated = len(rows) > MAX_RETURN
        matches = [(db.get(Incident, row.id), round(row.distance_m / 1000, 2))
                   for row in rows[:MAX_RETURN]]
        return GeoSearch(matches, "postgis_geography", truncated, MAX_RETURN)

    if backend not in ("portable", ""):
        raise ValueError("Unsupported geospatial backend")
    min_lat, max_lat, longitude_ranges = bbox(latitude, longitude, radius_km)
    conditions = [and_(Incident.longitude >= west, Incident.longitude <= east)
                  for west, east in longitude_ranges]
    stmt = (select(Incident)
        .where(
            Incident.latitude.is_not(None), Incident.longitude.is_not(None),
            Incident.latitude >= min_lat, Incident.latitude <= max_lat,
            or_(*conditions),
        )
        .order_by(Incident.created_at.desc(), Incident.id)
        .limit(MAX_SCAN + 1))
    candidates = db.scalars(stmt).all()
    truncated = len(candidates) > MAX_SCAN
    within_radius = []
    for report in candidates[:MAX_SCAN]:
        km = haversine_km(latitude, longitude, report.latitude, report.longitude)
        if km <= radius_km:
            within_radius.append((report, round(km, 2)))
    within_radius.sort(key=lambda result: (result[1], result[0].id))
    return GeoSearch(within_radius[:MAX_RETURN], "portable_bbox_haversine",
                     truncated or len(within_radius) > MAX_RETURN, MAX_SCAN)
