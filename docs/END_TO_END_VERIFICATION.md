# Full-stack integration and end-to-end verification

**Scope:** tests the local research portfolio application as software. A successful result is **not** a real government alert feed, validated hazard model, incident dispatch system, or officially approved public service.

## What is exercised

GitHub Actions runs a disposable Docker Compose stack with a PostgreSQL/PostGIS container, the FastAPI application, and a React frontend served by Nginx.

1. Start DB and wait for PostgreSQL healthcheck.
2. Start the API and wait for `/api/ready` to confirm it can reach the required database schema.
3. Start Nginx and wait for an HTTP response from the frontend service.
4. Request the compiled React HTML through Nginx, then request API endpoints **through the Nginx reverse proxy**.
5. Confirm `/api/v1/alerts` returns an explicitly disconnected official warning feed, rather than invented warnings.
6. Confirm the fictional scenario is deterministic, 24 hours long, and creates zero incident reports.
7. Confirm the isolated incident DB starts empty and a stale example risk input returns `unavailable`.
8. Confirm an arbitrary client-side route receives the React HTML shell (SPA fallback).
9. Shut down the entire disposable test stack and **remove only its CI-only database volume**.

## Run with Docker

Copy `.env.example` to `.env` and set a strong, URL-safe `POSTGRES_PASSWORD`, or use the provided Windows launcher. For Linux/macOS:

```bash
docker compose up --build -d --wait --wait-timeout 120
python scripts/smoke_compose.py --base http://127.0.0.1:5173
docker compose ps
```

On Windows PowerShell:

```powershell
.\scripts\start-local.ps1
python scripts/smoke_compose.py --base http://127.0.0.1:5173
```

Do **not** delete your local persistent DB volume when you finish; run `docker compose down` only. In ephemeral GitHub CI, removing volumes is safe and prevents test data lingering.

## What the smoke test does not test

- No real IMD/CWC source authentication, license, or up-to-date warning data.
- No validated disaster predictions or real storm-event training dataset.
- No approved human disaster-response organization, dispatch workflow, emergency triage or government authority.
- No public cloud hostname, real identity provider or professional penetration test.
- No browser-specific screen reader test or translation approval by native speakers.

## Diagnosing failures

- `docker compose ps` shows whether the database/API/web container is healthy.
- `docker compose logs --tail=120 db` diagnoses PostgreSQL initialization and password issues.
- `docker compose logs --tail=120 api` diagnoses API startup, DB configuration and Python dependencies.
- `docker compose logs --tail=120 web` diagnoses Nginx errors or proxy resolution.
- `docker compose config` checks YAML and interpolated environment settings locally. Be careful: this output can include your local DB password; **never paste it into public GitHub issues or screenshots**.

## Automated evidence

Check `.github/workflows/ci.yml` and the latest successful GitHub Actions **Docker Compose end-to-end acceptance** job. Its dedicated acceptance script is `scripts/smoke_compose.py`, which uses only the Python standard library and contains no network calls to outside official providers.
