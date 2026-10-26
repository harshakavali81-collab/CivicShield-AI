# Production setup — code preparation, not operational certification

## Identity and API
Provision a real OIDC provider with account registration, MFA and controlled assignment of the civicshield-responder role.
Required production environment variables:
- APP_ENV=production
- AUTH_MODE=oidc
- OIDC_ISSUER=https://your-idp.example
- OIDC_AUDIENCE=civicshield-api
- OIDC_JWKS_URL=https://your-idp.example/keys
- OIDC_RESPONDER_ROLE=civicshield-responder
- DATABASE_URL=postgresql+psycopg://...
- CORS_ORIGINS=https://your-frontend.example
- INCIDENT_SUBMISSIONS_ENABLED=false

Production startup refuses missing OIDC configuration, SQLite and enabled public reporting. OIDC verification validates RS256 signatures, exp, iss, aud and responder role. This code does not create accounts, host an IdP or implement browser sign-in: authorized clients must supply Bearer access tokens.

## Official weather sources
IMD district warning adapter supports the documented official schema. IMD_API_ENABLED remains false unless an operator confirms API access and permission. Provide a token only if your approved account requires that form. CWC offers official forecast website bookmarks only; no undocumented API is assumed.

## Deployment
Render blueprint render.yaml needs a connected Render account, billing selection, managed PostgreSQL, configured IDP, TLS/domain and frontend API URL. It is a template and has not been launched.
Manual GitHub Pages workflow can publish the separate safe informational site/ page after Pages > GitHub Actions is enabled. It does not host FastAPI or incident review.

## Research validation
python -m civicshield.ml.validate_external --data /path/to/labeled.csv --output artifacts/evaluation_reports/validation.json
The input requires observed_at,district,risk_label,rainfall_24h_mm,temperature_c,humidity_pct. Tests assess temporal and district holdouts but cannot establish label validity or scientifically reliable warnings.

## Not certified
IMD authorization, CWC machine-feed agreement, broad labeled data, real domain validation, account provisioning, public backend deployment, backups/recovery, privacy assessment and emergency authority approval are still necessary.