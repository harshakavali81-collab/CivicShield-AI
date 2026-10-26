# Operator runbook: local demonstration only

## Live modeled weather (Open-Meteo, not IMD)

The opt-in endpoint \`GET /api/v1/weather/live?latitude=17.38&longitude=78.48\` is disabled by default. Enable with \`OPEN_METEO_ENABLED=true\` in the shell or Docker \`.env\`.

It obtains temperature, humidity and a sum of available modeled hourly precipitation values over the preceding 24 hours. The provider timestamp and provenance are shown and an upstream outage results in HTTP 503, **not** a fabricated forecast. Longitude/latitude are rounded to two decimals. No more than one external call per 10 minutes is used for the same rounded coordinates within one process.

Open-Meteo's free service is for noncommercial use with attribution. See https://open-meteo.com/en/terms and https://open-meteo.com/en/docs . This API does **not** carry official government warnings or guarantee safety.

To save individual weather snapshots locally for an operator-managed schedule:

~~~bash
python -m scripts.collect_weather --latitude 17.38 --longitude 78.48
~~~

Rows append to gitignored \`data/raw/open_meteo_history.jsonl\`; operator must verify license, avoid personal-location collection and configure the recurring schedule themselves. No task is silently running.

## Access and protection

- \`INCIDENT_SUBMISSIONS_ENABLED=false\` (default) disables incident intake.
- \`REPORTER_API_KEY\` is an optional shared demo intake key. Set when enabling controlled demo reporting. UI includes a password field; keys are not stored by the browser component.
- \`RESPONDER_API_KEY\` is mandatory for review, audit, geospatial report queries and operational status.
- Per-process rate limit guards: 30 submitted reports / hour, 20 modeled-weather requests / hour, 120 knowledge searches / hour per socket peer. **Not distributed or production-ready.**
- Security headers: nosniff, no framing, no-referrer, no-store and restricted device permissions.
- Human status changes are recorded in a local audit table (no verified actor identity).
- \`GET /api/v1/ops/status\` (reviewer key): database check and configuration flags; never credentials.

## Backup, data quality and retention

~~~bash
python -m scripts.backup_sqlite --output backups/manual-backup.db
python -m scripts.purge_incidents --days 30
python -m scripts.purge_incidents --days 30 --confirm
python -m scripts.check_data_quality /path/to/your_labeled.csv
~~~

Backup writes a consistent copy of the SQLite demo database with restrictive local filesystem permissions. Backups can contain PII; do not upload them publicly. The purge command deletes both old report rows and their linked audit records. PostgreSQL operators must use \`pg_dump\` and establish separate restoration tests, encryption and retention policies.

## Database migrations and geospatial index

\`pip install -e ".[migrations]"\` then **on an empty database only** \`alembic upgrade head\`. API startup already performs \`create_all\` for local convenience; do not blindly run an initial migration on a database with existing tables. For a preexisting database, first reconcile the schema and use \`alembic stamp\` only when the schema actually matches.

An optional PostgreSQL/PostGIS index is in \`backend/migrations/postgis_indexes.sql\`. The reviewer-only \`/api/v1/incidents/nearby\` endpoint currently computes haversine distances for up to 5,000 candidates and returns at most 100, so it is not guaranteed exhaustive.

## Optional SHAP and MLflow

~~~bash
pip install -e ".[explain,tracking]"
python -c 'from civicshield.ml.experiment import log_experiment; print(log_experiment("artifacts/models/risk_model.metrics.json"))'
~~~

The SHAP helper accepts **trusted local joblib** artifacts only. Both tools are optional research utilities; no hosted tracking/registry or drift alerts are deployed.

## Production blockers

Shared-key review is not real OIDC/RBAC/MFA, in-memory limits do not scale, submissions lack independent moderation, and free-text redaction is incomplete. TLS, rate limiting, secure telemetry, retention policy, offsite encrypted backups, incident response, human-reviewed translations, model validation and source authority governance are still required.
