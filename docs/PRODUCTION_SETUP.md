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

## Browser OIDC public-client setup

Register a public OAuth/OIDC SPA client configured for Authorization Code + PKCE in the same provider that issued the API trust configuration. Set VITE_AUTH_MODE=oidc, VITE_OIDC_AUTHORITY, VITE_OIDC_CLIENT_ID and VITE_OIDC_SCOPE with a scope that produces an access token with the API audience and server-required responder role. The frontend handles the redirect and sends Bearer tokens only to restricted routes. Review provider consent, CORS, CSP, trusted domains and token storage carefully before public use; this is not a substitute for a security audit.


## Pseudonymous reviewer audit identities

A production installation must set a separate high-entropy `AUDIT_HASH_SECRET` with at least 32 characters, stored only in the hosting secret manager. The backend derives a stable HMAC-SHA256 reference from a verified OIDC issuer and subject without returning raw subject IDs. Local demo-key reviews remain unattributed. Changing the secret changes future actor references; document a controlled migration/retention process before rotation. HMAC alone is **not** user consent, an audit retention policy or proof that local users are properly authorized.

## JWKS endpoint trust and request traceability

By default the backend will only fetch OIDC JWKS signing keys from the **same HTTPS hostname** as the configured OIDC issuer. This prevents accidental JWKS URL drift and local/private IP endpoints. If a real provider intentionally hosts keys on a different DNS hostname, list the **exact approved hostname** in `OIDC_JWKS_ALLOWED_HOSTS` (comma-separated, no wildcards). Use HTTPS on the standard port 443 and verify the identity provider's published configuration. This checks URLs before fetching; it is **not** a defense against DNS rebinding, a cloud egress firewall, or a full IdP security review.

Each API response includes a randomly generated `X-Request-ID` for diagnostics. This value is generated on the server, never copied from a caller, and does not expose any token or personal incident detail. If instrumenting centralized logs later, log only this ID, endpoint template, status, and operation duration; do not log authorization headers, report content, coordinates or identity-provider credentials.
