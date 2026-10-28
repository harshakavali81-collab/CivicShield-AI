-- Optional PostGIS-only index for distance search of UNVERIFIED reports.
-- Requires CREATE EXTENSION privilege. Execute only after reviewing legal/privacy policies.
-- Use: psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f backend/migrations/postgis_indexes.sql
-- Enables GEOSPATIAL_BACKEND=postgis; NOT applied to ordinary Render PostgreSQL.
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE INDEX IF NOT EXISTS ix_incidents_geography_gist
ON incidents USING GIST (
  (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography)
)
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
