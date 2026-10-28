# CivicShield AI software portfolio release checklist

This checklist covers a **research demonstration and reproducible engineering artifact**. It is explicitly **not a certification for public disaster warning or emergency operations**.

## Automated green CI

GitHub Actions should verify:
- [ ] Python unit and integration tests (including provenance, review roles, HMAC identity, scenario simulation, readiness and stale input)
- [ ] Fresh SQLite migration through latest revision
- [ ] Real PostgreSQL/PostGIS migration and isolated radius-query smoke test
- [ ] React production build
- [ ] Backend and frontend Docker builds, Compose validation
- [ ] Integrated live Docker Compose HTTP acceptance of all three services
- [ ] Chromium UI tests (desktop navigation, responsive/mobile, keyboard, disconnected source and stale-input behavior)
- [ ] Static informational site asset/SVG checker before optional Pages deployment

Use [Actions](https://github.com/harshakavali81-collab/CivicShield-AI/actions) to confirm exact run status before claiming a release passed.

## Responsible presentation

- [ ] README hero, original SVG gallery, architecture and project tree render properly
- [ ] Scenario Lab says **FICTIONAL** and contains no fabricated official performance scores
- [ ] `python -m scripts.smoke_demo` returns read-only software checks
- [ ] Source links resolve to original IMD, CWC and NDMA homepages
- [ ] Public demo does not expose raw report narratives, identities or exact home locations
- [ ] Local environment secrets and private files are not in Git history

## External tasks (cannot be completed by code alone)

- [ ] Connect an owned cloud hosting account and provision database, domain and HTTPS
- [ ] Configure real OIDC identity provider, client registration, MFA, role policies and secure auditing
- [ ] Obtain **explicit** IMD/CWC source access/license agreements if using operational APIs
- [ ] Obtain legally permitted independently labeled multi-region hazard/outcome data
- [ ] Establish domain-expert validation, operational thresholds, ongoing incident monitoring, privacy/legal approval and public-service authorization
- [ ] Design backed-up and tested incident recovery and human escalation protocols

## Evidence standard

Do not claim that a successful CI badge, Docker image, simulated chart or preflight result proves a public system is safe. There is no real-world hazard prediction validation in the repository.
