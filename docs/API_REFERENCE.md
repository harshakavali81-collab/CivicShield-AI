# API reference — CivicShield AI (research demo)

Swagger at http://localhost:8000/docs . All endpoints are for demonstration, **not emergency warnings or dispatch**.

| Method | Endpoint | Protection / data |
| --- | --- | --- |
| GET | \`/api/health\` | Public liveness, no safety guarantee |
| GET | \`/api/v1/sources\` | Government source bookmarks only |
| GET | \`/api/v1/alerts\` | Official feed intentionally disconnected |
| GET | \`/api/v1/weather/sample\` | Synthetic example |
| GET | \`/api/v1/weather/live?latitude=17.38&longitude=78.48\` | Third-party modeled data; \`OPEN_METEO_ENABLED=true\`; per-process limited |
| POST | \`/api/v1/risk/estimate\` | Experimental user-input indicator |
| POST | \`/api/v1/assistant/ask\` | Curated five-language general guidance |
| GET | \`/api/v1/assistant/knowledge?q=flood\` | Source-linked curated English summaries |
| POST | \`/api/v1/incidents\` | Disabled by default; optional \`X-Reporter-Key\` |
| GET | \`/api/v1/incidents/review\` | \`X-Responder-Key\`; latest 100 reports |
| PATCH | \`/api/v1/incidents/{id}/review\` | \`X-Responder-Key\`; statuses verified/dismissed/needs_info |
| GET | \`/api/v1/incidents/audit\` | \`X-Responder-Key\`; latest 100 local review events |
| GET | \`/api/v1/incidents/nearby?latitude=17.38&longitude=78.48&radius_km=10\` | \`X-Responder-Key\`; limited unverified geo scan |
| GET | \`/api/v1/ops/status\` | \`X-Responder-Key\`; safe operational summary |
| GET | \`/api/v1/analytics/summary\` | Counts of local reports only |
| GET | \`/api/v1/analytics/trends\` | Local report counts over the past seven days |

## Sample risk input

~~~json
{"city":"Hyderabad","rainfall_24h_mm":68,"temperature_c":29,"humidity_pct":85,"forecast_age_hours":1}
~~~

Mode \`demonstration_heuristic\` returns an illustrative grouping only. Stale age >6 h becomes \`risk_level=unavailable\`. A user-trained model can return **uncalibrated** \`model_score\` if a trusted artifact is explicitly configured. All risk responses set \`is_official_warning=false\`.

## Incident submission

~~~json
{"title":"Fallen tree on public road","description":"A large fallen tree blocks the road near the park.","city":"Hyderabad","language":"en","latitude":17.38,"longitude":78.48}
~~~

Optional coordinates must be supplied together and are disclosed only to authorized reviewers, not the public analytics feed. A reporter access key is strongly recommended even on controlled local environments. A status of \`verified\` means *demo reviewer marked verified*, not the government or emergency services.

## Source-linked retrieval

~~~text
GET /api/v1/assistant/knowledge?q=flood
~~~

Responses contain document summary \`body\`, \`source_title\`, \`source_url\`, \`curated_date\`, \`translation_verified=false\` and \`live_retrieval=false\` metadata. They are **not** current validated official advisories.

## Headers and quotas

Demo intake: \`X-Reporter-Key\` if configured. Restricted endpoints: \`X-Responder-Key\`. Single process only; rate limits can be bypassed across multiple replicas. Do not expose API publicly without a full security review.
