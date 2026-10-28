# Changelog

All versions describe **software capabilities**, not certification or authorization to operate a public emergency service.

## Unreleased — End-to-end integration

### Bounded demo quota correctness

- Fixed a rate-limit bypass where exceeding 5,000 tracked client/bucket entries cleared every active usage history.
- Added expiry-only reclamation, 429 capacity refusal and Retry-After values while preserving original active per-client limits.
- Added isolated capacity/concurrency-contract tests and explicit documentation that this in-process guard does not replace a distributed abuse-prevention system.


### OIDC security, human-review consistency and real UI capture

- Restrict signing-key JWKS URLs to trusted external HTTPS origins, defaulting to the issuer's hostname; allow exceptions only through exact operator-controlled hostnames.
- Generate a new server-side `X-Request-ID` in responses for privacy-conscious traceability without logging incident narratives, credentials, or user-supplied tokens.
- Add optional `expected_status` on reviewer decisions; stale submissions return HTTP 409, preventing silent overwrites and stray audit records.
- Capture four **actual Chromium screenshots from synthetic CI data**, with visible not-live/fictional disclaimers, and upload them as a downloadable 30-day GitHub Actions artifact.
- These quality improvements do **not** establish an approved identity provider, real emergency authority, or hosted public alert service.



### Fully offline interactive research demonstration

- Added `site/demo.html` and `site/demo.js`: a dependency-free SVG timeline with keyboard-operable slider, accessible data table and four selectable walkthrough chapters.
- Exported browser-only synthetic data from the canonical deterministic Python case study to `site/scenario-data.js`.
- Added source-equality checks, allowlisted local script audit and three additional Chromium tests that open `file://` resources without an API, hosting account or network.
- The demo does **not** fetch government data, submit reports, issue warnings or validate scientific predictions.



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
