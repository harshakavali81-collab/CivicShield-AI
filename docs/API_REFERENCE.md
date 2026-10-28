# API reference — CivicShield AI (research demo)

Swagger at http://localhost:8000/docs . All endpoints are for demonstration, **not emergency warnings or dispatch**.

| Method | Endpoint | Protection / data |
| --- | --- | --- |
| GET | `/api/health` | Public process-only liveness, not database or official alert readiness |
| GET | `/api/ready` | Public DB/schema readiness, not disaster or warning readiness |
| GET | `/api/v1/sources` | Government source bookmarks only |
| GET | `/api/v1/alerts` | Official feed intentionally disconnected |
| GET | `/api/v1/weather/sample` | Synthetic example |
| GET | `/api/v1/weather/live?latitude=17.38&longitude=78.48` | Third-party modeled data; `OPEN_METEO_ENABLED=true`; per-process limited |
| POST | `/api/v1/risk/estimate` | Experimental user-input indicator |
| POST | `/api/v1/assistant/ask` | Curated five-language general guidance |
| GET | `/api/v1/assistant/knowledge?q=flood` | Source-linked curated English summaries |
| POST | `/api/v1/incidents` | Disabled by default; optional `X-Reporter-Key` |
| GET | `/api/v1/incidents/review` | `X-Responder-Key`; latest 100 reports |
| PATCH | `/api/v1/incidents/{id}/review` | `X-Responder-Key`; statuses verified/dismissed/needs_info |
| GET | `/api/v1/incidents/audit` | Reviewer auth (OIDC Bearer in configured deployments, demo key locally); pseudonymous actor references |
| GET | `/api/v1/incidents/nearby?latitude=17.38&longitude=78.48&radius_km=10` | Reviewer auth; optional PostGIS indexed geography or portable bounding-box/haversine search; unverified records only |
| GET | `/api/v1/ops/status` | `X-Responder-Key`; safe operational summary |
| GET | `/api/v1/analytics/summary` | Counts of local reports only |
| GET | `/api/v1/analytics/trends` | Local report counts over the past seven days |

## Sample risk input

~~~json
{"city":"Hyderabad","rainfall_24h_mm":68,"temperature_c":29,"humidity_pct":85,"forecast_age_hours":1}
~~~

Mode `demonstration_heuristic` returns an illustrative grouping only. Stale age >6 h becomes `risk_level=unavailable`. A user-trained model can return **uncalibrated** `model_score` if a trusted artifact is explicitly configured. All risk responses set `is_official_warning=false`.

## Incident submission

~~~json
{"title":"Fallen tree on public road","description":"A large fallen tree blocks the road near the park.","city":"Hyderabad","language":"en","latitude":17.38,"longitude":78.48}
~~~

Optional coordinates must be supplied together and are disclosed only to authorized reviewers, not the public analytics feed. A reporter access key is strongly recommended even on controlled local environments. A status of `verified` means *demo reviewer marked verified*, not the government or emergency services.

## Source-linked retrieval

~~~text
GET /api/v1/assistant/knowledge?q=flood
~~~

Responses contain document summary `body`, `source_title`, `source_url`, `curated_date`, `translation_verified=false` and `live_retrieval=false` metadata. They are **not** current validated official advisories.

## Headers and quotas

Demo intake: `X-Reporter-Key` if configured. Restricted endpoints: `X-Responder-Key`. Single process only; rate limits can be bypassed across multiple replicas. Do not expose API publicly without a full security review.


## Geographic search mode

Set `GEOSPATIAL_BACKEND=portable` (default; works with local SQLite or ordinary PostgreSQL) or explicitly enable `postgis` **only on a PostgreSQL database with PostGIS installed and the matching geography index**. The payload contains `search_backend`, `possibly_incomplete`, `scanned_limit`, `radius_km` and results sorted by distance. Portable mode has a 5,000-candidate bound and output is capped at 100. Do not treat the results as an exhaustive list of real hazards.

## Reviewer identity and local safety

Restricted review endpoints accept `X-Responder-Key` only in local demo mode. With configured `AUTH_MODE=oidc`, the server requires an RS256-signed Bearer token with correct issuer, audience, expiry and responder role. Audit stores a pseudonymous `actor_ref` derived from issuer and subject, or `local_demo_shared_key` for local demo mode. It is **not** a verified audit of individual local key holders. No raw OIDC tokens or subject names are returned in audit API output.

## Quick read-only software smoke check

```bash
python -m scripts.smoke_demo --url http://localhost:8000
```

This command tests health/readiness, source disconnection, the synthetic-weather label, stale experimental input and curated source retrieval. It never posts an incident or calls official live government APIs.
