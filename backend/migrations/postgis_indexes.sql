-- Optional PostGIS-only spatial indexing of unverified reports.
-- Run manually on a controlled local PostgreSQL/PostGIS database.
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE INDEX IF NOT EXISTS ix_incidents_geo_gist
ON incidents USING GIST (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326))
WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
