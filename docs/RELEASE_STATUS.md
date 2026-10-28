# CivicShield AI — factual release status

This report separates tested software from unverified external operational dependencies. It is a **research portfolio release**, not an emergency warning service.

## Implemented, reproducible and under automated tests

- [x] FastAPI research API, source-provenance metadata, weather/model input guards
- [x] React dashboard with trends, illustrative maps, guidance, optional sources and fictional Scenario Lab
- [x] Human-only demo report moderation, reviewer access control and audit references
- [x] SQLite / PostgreSQL migrations; optional PostGIS geospatial calculations
- [x] Docker Compose with PostgreSQL/PostGIS + API + Nginx/React; startup healthchecks
- [x] Backend unit/integration tests and API smoke tests
- [x] Real full-stack Docker Compose HTTP acceptance testing
- [x] Chromium Playwright UI scenarios for desktop/mobile and keyboard interactions
- [x] Offline GitHub Pages informational site with original SVG assets and static-site safety tests
- [x] Deployment preflight CLI with no printed secrets
- [x] Developer runbooks, model-card boundaries, data-safety rules, CI workflows, case study, diagrams

The source of truth for the latest pass/fail status is [GitHub Actions](https://github.com/harshakavali81-collab/CivicShield-AI/actions). Do not claim a successful run without its commit and job results.

## External prerequisites — intentionally NOT marked complete

- [ ] **Public static website** — repository owner must select GitHub Actions under Settings → Pages and manually run the prepared publish workflow. No public URL is claimed until successful deployment is verified.
- [ ] **Public backend hosting** — requires a cloud account, secrets, cost/region decisions, managed database, TLS, backup and monitoring policy.
- [ ] **Real identity provider** — account registration, OIDC audience, JWKS, MFA and role policies need an actual provider and qualified administration.
- [ ] **Official data authorization** — IMD/CWC API contracts, credentials and reuse permission have not been obtained; public alert feed remains disconnected.
- [ ] **Scientific validation** — no independently labeled multi-region real disaster outcomes or qualified domain certification are present.
- [ ] **Operational approval** — public incident intake, security/privacy impact review, disaster recovery, accessibility evaluation and emergency-authority partnerships are pending.

## Interpretation

Successfully building, running, testing or publishing an educational portfolio does **not** authorize emergency instructions, evacuation decisions or predictions of safety. Unknown, missing, stale or disconnected upstream information must never be treated as an all-clear.
