# Quality assurance: verified CI and manual tests

## Automated workflows

~~~bash
python -m pip install -e ".[dev,migrations]"
pytest -q
python -m compileall -q backend src scripts
DATABASE_URL=sqlite:///./migration_ci.db alembic upgrade head
cd frontend && npm install && npm run build
~~~

GitHub Actions runs API tests, compilation, an isolated fresh SQLite migration smoke test and React production build on pushes and PRs.

| Area | Automated assertions |
| --- | --- |
| Weather | Provider JSON normalization, minimum 24h coverage, stale-input fail-closed, cached request behavior, no official warnings |
| Risk | Schema, heuristic grouping, stale data, missing trusted model |
| Knowledge | Multilingual educational responses and source-backed English retrieval |
| Report handling | Submission opt-in, reporter key, contact redaction, duplicate flag, validation and role protections |
| Review | Human status update, audit record, reviewer restricted geolocation scan |
| Privacy | Retention dry-run, report + audit deletion |
| Operations | Health/status, security headers, SQL backup, collector JSONL, data-quality checks |
| ML | Labeled input validation, split/class checks and artifact serialization |
| Graphs | SVG confusion matrix and classification-metric rendering |
| Frontend | Vite bundle successfully builds |
| Migrations | Alembic upgrade on clean throwaway SQLite |

## Manual acceptance checklist

1. Start FastAPI and React. Check overview and all navigation tabs at desktop and mobile widths.
2. Confirm map markers are **illustrative only**.
3. Enter stale risk values (>6 h). It must return unavailable, never safe.
4. Enable modeled weather intentionally. Fetch weather and verify attribution, timestamps, optional caching and disconnected official warning status.
5. Exercise five-language prepared guidance and curated document search.
6. With submissions disabled, verify 503. In an isolated local environment enable intake/reviewer keys and submit a fake report.
7. Review the record, inspect audit log, and query nearby using optional sample coordinates.
8. Verify rate limits and wrong keys fail; verify private narratives/coordinates never appear in public endpoints.
9. Perform a SQLite snapshot and dry-run retention purge on expendable test data.
10. Review WCAG focus, contrast, screen-reader map alternative and native-script translations with human testers.

## Still missing for a real service

True domain-labeled data, calibrated geographic model validation, secure distributed authentication/rate limits, internationalized accessibility review, simulated disasters/chaos testing, consent/retention compliance and independently approved official feed operations.
