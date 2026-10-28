# Changelog

All versions describe **software capabilities**, not certification or authorization to operate a public emergency service.

## Unreleased — End-to-end integration

### Shareable portfolio and cloud template verification

- Checked Render Blueprint against updated database plan identifiers, explicit cost warnings, application rewrite rules and restrictive defaults.
- Added automated structural checks for render.yaml to catch unsafe operational changes.
- Added reproducible self-contained static portfolio ZIP + checksum, produced as a short-lived GitHub Actions artifact.
- **Still external:** actual provider provisioning, charges/plan approval, identity provider, real weather permissions and model validation.



### Browser and static-site quality gates

- Added five Playwright Chromium tests running against the complete containerized React+FastAPI stack.
- Added desktop/mobile keyboard navigation, skip links, active-page descriptions and reduced-motion support.
- Finished static GitHub Pages portfolio assets and added automated SVG integrity/accessibility checks before publishing.
- Added factual release status and owner publishing instructions. **No production service or public URL is implied.**



- Added Docker Compose health-gated startup and a dedicated five-job CI pipeline.
- Added eight read-only HTTP acceptance checks through the compiled React/Nginx reverse proxy and real PostgreSQL/PostGIS.
- Added local-stack troubleshooting and Windows launcher readiness verification.
- The integration check uses deliberately fictional data and cannot certify a real emergency service.

## 0.2.0 — 2026-10-28 (portfolio feature release)

- Added reproducible fictional 24-hour case-study generator, REST endpoint, interactive Recharts visualizations and guided source/review/ML walkthrough.
- Added read-only deployment preflight CLI with pass/blocking status and no secret disclosure.
- Strengthened reviewer identity references with a production HMAC secret requirement and clear demo-key attribution limitations.
- Added scenario, deployment and audit security regression tests to Python CI.
- Continued automated frontend, backend, PostgreSQL/PostGIS, migrations and Docker image build verification.
- Updated README with original vector-graphic gallery and documented project architecture.

**Not delivered:** actual independent disaster prediction validation, government approval, IMD/CWC credentials, fully deployed cloud identity/hosting or emergency-service certification.

## 0.1.0 — 2026-10 (initial research demonstration)

- Built the FastAPI/React dashboard, synthetic risk indicator, educational multilingual guidance, human report moderation, local DB, optional third-party modeled weather and official-source reference boundaries.
- Added Docker Compose, Alembic schema migrations, PostGIS research queries, OIDC client/server integration scaffolding, report privacy tools and comprehensive source documentation.
