# Render deployment blueprint — researched template, not a live account

The repository contains a `render.yaml` describing **a paid managed Postgres database, a Docker/FastAPI web API and a React static web frontend**. As of October 2026, the database plan uses Render's modern `0.5c-1g` plan ID. The API's `starter` legacy plan remains supported by Render. Creating these resources **can incur charges**; provisioning, agreeing to fees, connecting an identity provider and enabling a domain are operator actions, not tasks performed by the code.

The configuration has been checked against [Render's Blueprint reference](https://render.com/docs/blueprint-spec) and is subjected to local structural and safety tests. It has **not** been tested with an owned Render account.

## Before provisioning

1. [Review Render's current pricing](https://render.com/pricing) and confirm that the proposed account/region/DB plan are acceptable.
2. Provision an actual OIDC identity provider. Register a confidential backend resource/API audience and a **public SPA client using Authorization Code + PKCE**. Require MFA and tightly managed `civicshield-responder` role assignment.
3. Decide on the URL of the frontend and backend, and choose HTTPS-only deployment. The `VITE_API_BASE` frontend environment variable is resolved **at build time**; it must reference the actual HTTPS API origin. The `CORS_ORIGINS` backend variable must list the matching HTTPS frontend origin.
4. Set `OIDC_ISSUER`, `OIDC_AUDIENCE`, `OIDC_JWKS_URL`, `CORS_ORIGINS` and the frontend OIDC variables using Render's secure setup prompts. The `AUDIT_HASH_SECRET` is provider-generated and must not be committed.
5. Keep `INCIDENT_SUBMISSIONS_ENABLED=false`, `IMD_API_ENABLED=false` and `OPEN_METEO_ENABLED=false` until explicit independent authorization and privacy review. The deployment must never be advertised as an emergency warning service.

## Validate locally (no account or fees)

```bash
python -m pip install -e ".[dev,migrations]"
python -m scripts.validate_blueprint
python -m scripts.doctor --mode production --json
```

The doctor will intentionally fail if your *real operator environment variables* are not set. Do not paste secret-bearing environment output into GitHub issues.

## Deploy manually

Use [Render's Blueprint flow](https://render.com/docs/infrastructure-as-code) and select this GitHub repository. Review each compute/database plan and expense before creating any service. Automatic deploys are disabled in the Blueprint to avoid unreviewed changes. If the provider validates and accepts the Blueprint:

- Run the database migration pre-deploy command: `python -m alembic upgrade head`.
- Check API readiness `/api/ready`; this confirms DB/schema only, not government source availability.
- Build the frontend with HTTPS `VITE_API_BASE` and verified OIDC public-client details.
- Complete approved OIDC sign-in and reviewer-role tests with your own identity provider. Do not test with real citizen information.
- Check backend and frontend headers, CORS, error handling, billing, backups, logging retention and privacy threat model.

**No live Render URL, authenticated OIDC tenant, IMD data access, CWC feed, public incident service, or validated disaster model is currently verified in this project.**

## GitHub downloadable alternative

You can share a **fully offline static project showcase** without creating a hosting account. Every successful CI run now stores `civicshield-offline-portfolio-v0.2.0.zip` and its SHA-256 checksum as a downloadable artifact for 30 days. It contains the self-contained `site/` portfolio, with original SVG illustrations and project links, but not the runnable Python/React platform.

See [GitHub Actions](https://github.com/harshakavali81-collab/CivicShield-AI/actions/workflows/ci.yml). Open a successful run → **Artifacts** → `civicshield-offline-portfolio-v0.2.0`, extract the ZIP and open `index.html`. You can verify the SHA-256 locally before extracting; checksums are integrity tools, not publisher digital signatures.
