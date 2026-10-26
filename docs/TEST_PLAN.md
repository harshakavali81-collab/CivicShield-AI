# Quality and safety test plan

Run from repository root:

~~~sh
pip install -e ".[dev]"
pytest -q
python -m compileall -q backend src
cd frontend && npm install && npm run build
~~~

## Automated coverage

| Area | Checks |
| --- | --- |
| API health and sources | Explicit demo mode, sources not connected |
| Weather/risk | Valid labels, stale unavailable, schema errors, no official warning |
| Assistant | Five response languages, reference attribution, unsupported language |
| Incident intake | Validation, opt-in only, duplicates not suppressed, privacy redaction |
| Responder | Missing/wrong key rejected, successful human update |
| Training | Binary labels, sample size guard, temporal holdout, serialized artifact |
| Continuous integration | Backend tests + frontend production bundle |

## Manual browser test

1. Navigate all six tabs on desktop and mobile sizes.
2. Check dashboard synthetic-chart warning and illustrative-only map markers.
3. Submit a stale forecast (7h) and confirm the risk response is unavailable.
4. Ask flood questions in five languages; verify responses and official reference links.
5. With intake disabled, confirm an explanatory error; in local opt-in mode submit a sample report.
6. Verify missing reviewer key is rejected; configured key displays queue and can set status.
7. Reload dashboard to confirm stored counts update.
8. Verify page never says "safe" based on missing alert feed.
9. Test keyboard focus, screen readers, color contrast and local language fonts before public tests.

## Mandatory real-world acceptance criteria (NOT met)

External weather provenance, independent spatial evaluation, safety review, public accessibility tests, authentication and user privacy controls, documented availability targets, secure TLS deployment, backups and incident response.
