# Safety, privacy and threat model

> Never use this demo to trigger alerts, evacuations, rescue or prioritization of real emergency resources.

## Guardrails implemented

- API labels experimental estimates and false official-warning status.
- Weather data older than six hours produces **unavailable** not a low risk score.
- No automatic official notices are invented; API discloses alert feed disconnect.
- Public incident intake disabled unless explicitly opted in.
- Pydantic validation, field size limits and SQLAlchemy bound queries.
- Basic email/phone pattern redaction before incident storage (not comprehensive PII detection).
- No public route reveals incident coordinates, title, description or reporter information.
- Human review cannot be performed without an explicitly configured local reviewer API key.
- Exact duplicates are flagged but NEVER automatically suppressed.
- Model loading is opt-in and documented as unsafe for untrusted joblib files.

## Known limitations / security blockers for internet deployment

- **Authentication:** one shared static key, no per-user roles, MFA, revocation or audit log.
- **Abuse:** no rate limiting, spam filtering, image verification, anti-bot or CSRF review.
- **Privacy:** free text may contain unrecognized names, addresses and identifiers; geolocation requires retention controls and encryption.
- **Storage:** no migration system, encryption-at-rest policy, backups, incident deletion controls or retention schedule.
- **Serving:** demo-only HTTP on localhost, no configured HTTPS, security headers or secure origin policies.
- **Maps:** visiting OpenStreetMap tiles contacts a third-party map service.
- **ML:** no true model validation/calibration/drift measurement or incident prioritization safety review.
- **Accessibility/localization:** human review of translations and WCAG testing not done.
- **Alert operations:** no real-time official feed, no authoritative confirmation, no 24/7 on-call or emergency service arrangement.

## Key threats

| Threat | Impact | Required mitigation |
| --- | --- | --- |
| Fabricated reports | Misleading reviewers | Rate limits, identity validation, moderation, audit |
| PII exposure | Citizen harm | Retention policies, RBAC, encryption, redaction |
| Model false negative | Unsafe reassurance | No safety conclusions; independent evaluation |
| Stale weather data | Wrong indicator | Freshness guard, fail-closed |
| Spoofed official alert | Severe misinformation | Official source signatures/validation; verified provenance |
| Leaked reviewer API key | Unauthorized actions | OIDC, least privilege, secret rotation, audit |
| Joblib malicious file | Code execution | Never load untrusted models, artifact signing |

## Emergency notice

Use relevant official emergency communications and the appropriate local emergency number. Do not depend on this application.
