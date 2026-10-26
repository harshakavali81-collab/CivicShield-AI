# Roadmap and honest implementation status

**Implemented in repository:** Python FastAPI backend, Pydantic contracts, local SQL storage, PostgreSQL Compose option, opt-in supervised experiment, freshness gates, basic incident review with demo key, curated translations, interactive React/Leaflet, synthetic charts, tests, docs and CI.

**Not yet delivered:**
- [ ] Real weather provider API authentication, ingestion scheduler, provenance and stale source monitoring
- [ ] Defensible flood/heat targets backed by sufficiently broad licensed labeled datasets
- [ ] Independent cross-region, temporal, severity, recall and calibration evaluation
- [ ] Provenance-backed multilingual RAG and approved document ingestion with freshness/version controls
- [ ] Human-vetted translations and localization usability studies
- [ ] PostGIS geometry indexes, spatial queries, robust migrations
- [ ] SHAP explanation pipeline with leakage/fairness checks
- [ ] Real MLflow tracking/registry and drift monitors
- [ ] OIDC/RBAC/MFA, security headers, API rate limits, moderation, audit trail
- [ ] Retention/deletion policy, encryption, backups, disaster-recovery tests
- [ ] Live integration tests and accessibility/WCAG checks
- [ ] Secure hosted demonstration without report submission or sensitive data
- [ ] Official emergency authority partnership and validation (outside portfolio scope)

## Milestones

1. Stabilize demo CI + secure local packaging.
2. Acquire authorized external data and build real temporal/geographic benchmarks.
3. Implement authenticated data provenance and official-source ingestion (without generating alerts).
4. Build RAG corpus with audited approved sources and translation quality gates.
5. Add production-grade identity, abuse defenses, privacy controls and monitored hosting.
6. Seek expert review before describing models as useful decision support in the real world.

This roadmap explicitly separates runnable prototype capability from aspiration.
