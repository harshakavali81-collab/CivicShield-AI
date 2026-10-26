# CivicShield AI — implementation status and remaining engineering gates

**As of 2026-10-26:** runnable local research/portfolio demo. This repository is not approved for emergency-response or public disaster-warning use.

## Delivered and tested

- [x] FastAPI, Pydantic contracts, SQLAlchemy SQLite/PostgreSQL, Docker/React/Leaflet/graphs
- [x] Demonstration rainfall thresholds with fail-closed six-hour freshness check
- [x] Optional labeled supervised classification experiment with chronological holdout and evaluation report
- [x] Optional local SHAP helper and MLflow experiment logger (requires optional dependencies; not production MLOps)
- [x] Opt-in non-authoritative, modeled live weather from Open-Meteo, with time/source/license attribution, timeout, rounding and 10-minute cache
- [x] One-shot CLI weather collector for use with an operator's external scheduler (not autonomous alerts)
- [x] Curated multilingual safety guidance in five languages and searchable English curated-source document summaries
- [x] Incident categorization, duplicate flagging and local authenticated human-only review
- [x] Reviewer audit history and restricted location-radius search, plus optional PostgreSQL PostGIS index recipe
- [x] Basic HTTP security headers, input bounds, demo reporter key and per-process rate limits
- [x] SQLite backup and local retention purge tool that also deletes linked reviewer audit entries
- [x] Initial Alembic empty-database migration; continuous migration smoke test
- [x] Synthetic demo map and actual local-report trends with clear provenance labels
- [x] Automated API/security/ML/backend and frontend build tests in GitHub Actions
- [x] READMEs, workflows, Mermaid graphs, SVG architecture illustration, graph generator, bookmarks and demo script

## Remaining work requiring external access or substantial domain engineering

- [ ] Official IMD/CWC alert feed credentials, contractual rights, verification and integration; **official alert feed remains DISCONNECTED**
- [ ] Large independent, permitted, labeled, region-diverse weather/hazard datasets with expert target definition and external validation
- [ ] Spatial/temporal cross-validation, probability calibration, lead-time evaluation, false-negative audits, stress tests and domain approval
- [ ] Authorized continuously updated multilingual retrieval corpus, source versioning and permission review; currently static curated summaries, not a generative RAG assistant
- [ ] Native-speaker review of multilingual guidance and accessibility/usability field studies
- [ ] End-to-end PostgreSQL/PostGIS optimized geospatial queries (current nearby search performs a bounded server-side scan)
- [ ] Production MLOps monitoring, model registry, retraining governance, alert policies and rollback
- [ ] Actual OIDC/RBAC/MFA, account identity, abuse prevention across replicas, web security review and encrypted data storage
- [ ] Automated backup schedule, offsite encrypted backups, recovery drills, legal retention consent and deletion compliance
- [ ] Hardened production HTTPS deployment and on-call monitoring; currently localhost Docker/development only
- [ ] Partnerships, official review and legally authorized public emergency operations (outside this portfolio project)

## Important distinctions

- Live modeled weather is **not** a government warning or direct station measurement.
- A locally trained RandomForest experiment is **not** a validated flood forecast.
- Curated local retrieval is **not** a live official bulletin or LLM-generated RAG answer.
- Human review status in a demo is **not** government confirmation.
- Generated plots are not evidence of real disaster-risk prediction accuracy.

## Priority order

1. Preserve green CI, dependency/security maintenance and local demo reliability.
2. Add licensed external data and independently evaluate actual supervised targets.
3. Implement verified source provenance and trusted feed governance.
4. Introduce real identity, privacy protections, monitoring and secure deployment.
5. Seek qualified meteorology/disaster-management review before *any* live decision-support claims.
