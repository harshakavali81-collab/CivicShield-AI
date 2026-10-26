# Operators: local monitoring, provenance and privacy

This is a local-only educational demonstration. **Do not expose it as an emergency dispatch or warning service.**

## Modeled real-world weather, not alerts

- \`GET /api/v1/weather/live?latitude=17.38&longitude=78.48\` calls Open-Meteo only when \`OPEN_METEO_ENABLED=true\`.
- Requests round latitude/longitude to two decimal places before sending to Open-Meteo.
- Up to 24 hours of *modeled* hourly precipitation is accumulated if >=20 periods are available. It is **not station-observed rainfall**.
- Data is cached 10 minutes and explicitly marked third-party modeled weather, timestamped and attributed. Failure produces HTTP 503, never invented substitute data.
- Free API is non-commercial with limits and no SLA; paid or self-hosted operation is required in other circumstances. Visit https://open-meteo.com/en/terms .
- Weather values must **not** be passed automatically to the flood-risk endpoint as though they were validated ground truth. The risk model remains experimental.

## Lightweight controls

- \`INCIDENT_SUBMISSIONS_ENABLED=false\` by default; enable only in controlled environments.
- \`REPORTER_API_KEY\` optional demo gate; set it whenever enabling local submissions.
- \`RESPONDER_API_KEY\` mandatory for review and reviewer audit (demo shared key).
- Fixed-window in-process limits guard report and knowledge endpoints; **not suitable for multi-instance production**.
- API security headers reduce exposure but do not implement TLS, secure sessions or real RBAC.
- \`GET /api/v1/ops/status\` requires responder key; summarizes DB status and configured feeds without disclosing secrets.
- \`GET /api/v1/incidents/audit\` requires responder key and shows local review audit trail.

## Privacy retention

Review and retention deletion are reversible only from a backup. Before running:

~~~sh
python -m scripts.purge_incidents --days 30
python -m scripts.purge_incidents --days 30 --confirm
~~~

This purges aged report entries but does not yet cascade all audit metadata; purge policies and backups need expert review. Rotate keys and avoid real personally identifying details during demo tests.

## Dataset quality

~~~sh
python -m scripts.check_data_quality /path/to/history.csv
~~~

Output highlights class balance, invalid timestamps, duplicate timestamps, missing values and provenance limitations.

## Optional interpretability and experiment tracking

~~~sh
pip install -e ".[explain,tracking]"
python -c 'from civicshield.ml.experiment import log_experiment; print(log_experiment("artifacts/models/risk_model.metrics.json"))'
~~~

SHAP helper: \`civicshield.ml.explain.explain("/trusted/path/risk_model.joblib", {"rainfall_24h_mm":60,"temperature_c":30,"humidity_pct":75})\`. Only load locally trusted model artifacts.

MLflow and SHAP are **optional** and not a deployed MLOps service. Measured model utility still needs scientific validation.
