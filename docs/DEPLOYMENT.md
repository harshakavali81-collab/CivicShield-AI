# Local demo deployment — NOT approved for public emergency use

## Prerequisites

Python 3.11+, Node 20+ or Docker/Compose; repository clone.

## Development

~~~bash
python -m venv .venv
# Activate the environment (Windows: .venv\Scripts\activate)
python -m pip install -e ".[dev,migrations]"
uvicorn backend.app.main:app --reload
~~~

In another shell:

~~~bash
cd frontend
npm install
npm run dev
~~~

Dashboard http://localhost:5173 ; Swagger http://localhost:8000/docs .

By default the simulated risk endpoint works offline. The separate real third-party modeled weather tab requires setting \`OPEN_METEO_ENABLED=true\` in the environment **before** starting the API.

## Docker local development

~~~bash
cp .env.example .env
# Edit .env to set POSTGRES_PASSWORD to a strong local-only string.
# Set OPEN_METEO_ENABLED=true if you explicitly want modeled third-party weather.
docker compose up --build
~~~

Docker publishes the API and UI to \`127.0.0.1\` only. \`.env\` is gitignored. Do not enable report submissions without a privacy review and local access key.

Set \`INCIDENT_SUBMISSIONS_ENABLED=true\`, \`REPORTER_API_KEY\`, and \`RESPONDER_API_KEY\` to exercise the demo intake/review flow. Do not distribute these keys or place them in an HTML bundle.

## Database maintenance

On a **new, empty** database only: \`alembic upgrade head\` after installing the \`migrations\` optional dependency. Existing databases initialized by API \`create_all\` require careful schema reconciliation before stamping or migration.

\`python -m scripts.backup_sqlite\` supports local SQLite only. PostgreSQL requires \`pg_dump\` and tested restore procedures.

## Model training and graphs

~~~bash
python -m civicshield.ml.train --data /path/to/labeled_history.csv --output artifacts/models/risk_model.joblib
python scripts/plot_metrics.py artifacts/models/risk_model.metrics.json
~~~

The training file must be independently labeled and legally sourced; no genuine hazard model is pre-trained or hosted.

## Production blockers

Missing public-trust infrastructure: secure identity/roles, rate limiting, moderation, encryption, TLS, official alert verification, actual validated hazard models, geospatial query optimization, safe human operational workflow and 24/7 monitoring. Never advertise this demo as a working emergency-warning service.
