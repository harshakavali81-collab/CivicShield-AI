# API reference

Local interactive Swagger: http://localhost:8000/docs

Base: \`http://localhost:8000\`

| Method | Route | Access | Description |
| --- | --- | --- | --- |
| GET | \`/api/health\` | Public | Demo status and UTC timestamp |
| GET | \`/api/v1/sources\` | Public | Reference catalog, integration state |
| GET | \`/api/v1/alerts\` | Public | Empty/not-connected official feed (not a safety statement) |
| GET | \`/api/v1/weather/sample\` | Public | Synthetic example observations |
| POST | \`/api/v1/risk/estimate\` | Public | Experimental rainfall-based indicator |
| POST | \`/api/v1/assistant/ask\` | Public | Curated multilingual preparedness advice |
| POST | \`/api/v1/incidents\` | Operator-enabled | Submit a sanitized non-emergency report |
| GET | \`/api/v1/incidents/review\` | Reviewer API key | Latest 100 reports incl. restricted content |
| PATCH | \`/api/v1/incidents/{id}/review\` | Reviewer API key | Human decision |
| GET | \`/api/v1/analytics/summary\` | Public | Aggregate counts |
| GET | \`/api/v1/analytics/trends\` | Public | Synthetic demonstration series |

## Prediction request

~~~json
{"city":"Hyderabad","rainfall_24h_mm":68,"temperature_c":29,"humidity_pct":85,"forecast_age_hours":1}
~~~

- \`forecast_age_hours>6\`: risk level \`unavailable\`, \`data_stale=true\`.
- No model configured: \`model_mode=demonstration_heuristic\`; rainfall illustrative thresholds; NOT flood predictions.
- Trusted local joblib configured: \`model_mode=user_trained_experimental\` and uncalibrated \`model_score\`; beware pickle trust.
- \`is_official_warning\` is always false.

## Incident submission

~~~json
{"title":"Tree blocking street","description":"A large fallen tree is blocking the road","city":"Hyderabad","language":"en"}
~~~

Submissions default to disabled (HTTP 503), and should **not** be enabled on a public site without authentication, rate limiting, moderation and a privacy review.

## Reviewer authentication

Send \`X-Responder-Key: <your locally configured RESPONDER_API_KEY>\`.
This is demo auth only; requires HTTPS, RBAC/OIDC and operational policy before deployment. Never put reviewer keys in repository or browser bundles.

## Assistant request

~~~json
{"question":"What should I do during a flood?","language":"te"}
~~~

Supported \`language\`: en, te, hi, ta, kn. Uses **curated/static** summaries with source bookmarks, not live official guidance.
