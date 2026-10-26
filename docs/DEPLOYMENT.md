# Local deployment and operational limitations

## Prerequisites

- Python 3.11+; Node 20+; or Docker + Docker Compose
- Git clone of repository
- Never store real credentials in Git

## Development

~~~sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn backend.app.main:app --reload
~~~

In a separate terminal:

~~~sh
cd frontend
npm install
npm run dev
~~~

API: http://localhost:8000/docs. UI: http://localhost:5173.

## Docker demo

~~~sh
cp .env.example .env
docker compose up --build
~~~

Docker includes PostgreSQL/PostGIS. The current SQLAlchemy schema stores numeric coordinates but does not yet use PostGIS spatial indexes or geometry types. Docker publishes the UI/API to loopback only.

For **local sample reporting**, place \`INCIDENT_SUBMISSIONS_ENABLED=true\` in \`.env\`, and set \`RESPONDER_API_KEY\` to a long random string; restart Compose. If you use Compose's Postgres database, set a different strong \`POSTGRES_PASSWORD\` variable in \`.env\` before database initialization.

Do not expose any part of this Compose stack to the public internet: default credentials, missing rate limits, demo auth and privacy-policy gaps make it unsafe.

## Optional trusted ML model

~~~sh
python -m civicshield.ml.train --data /absolute/path/owned_labeled.csv --output artifacts/models/risk_model.joblib
~~~

Set \`CIVICSHIELD_MODEL_PATH\` for backend local execution. The Compose API image does not include the training artifact by default. Joblib is pickle-based and can execute code on load; only use your own files. Not officially validated.

## Production readiness checklist

External ingress with TLS; identity/authz/roles; anti-abuse gates; validated live official sources; licensing; high availability; metrics; database migrations; PostGIS spatial implementation; backups/retention; consent; pen test; multilingual quality review; expert-validated hazard models; on-call processes; incident-response plan. These are **not implemented or claimed**.
