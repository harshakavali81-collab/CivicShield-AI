# Security policy

CivicShield AI is a **research and portfolio demonstration**, not an emergency or public warning service. Do not send real private incident data to an instance without separate legal authorization, a security review and a privacy plan.

## Reporting security issues

Please **do not post vulnerabilities, secrets, attack payloads, victim data, or government API credentials in public GitHub issues**. Use GitHub's private vulnerability reporting feature if enabled in this repository, or contact maintainers via a verified private channel shown on the GitHub profile. Do not assume a public contact mailbox is secure.

## Security boundaries

- Local demo auth uses shared keys and does not prove an individual reviewer's identity.
- Optional production OIDC verifies signature, issuer, audience, expiration and a configured role. An external identity provider must provision accounts, MFA and policies.
- OIDC audit references are keyed HMAC pseudonyms with the private `AUDIT_HASH_SECRET` in production; they are not anonymous.
- Report intake is off by default, and incomplete redaction should not be treated as privacy compliance.
- A single-process request limiter is not a production abuse-prevention mechanism.
- This app has no government permission to issue hazard warnings, rescue instructions, or all-clear notices.
- Optional weather/IMD clients intentionally fail closed on unavailable or invalid data.

## Deployment and secret rules

Never commit `.env` files, cloud credentials, model artifacts from untrusted parties, raw personal reports, database backups, API keys, IdP secrets or report attachments. Use a managed secret store and restricted-access backups. Review third-party data licenses and security incidents before publicly exposing any service.

For an offline configuration checklist:

```bash
python -m scripts.doctor --mode local
python -m scripts.doctor --mode production --json
```

Passing a preflight check **does not** certify real source rights, domain-model correctness, hosting security or operational safety.
