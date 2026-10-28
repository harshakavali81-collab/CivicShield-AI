# CivicShield AI — complete current repository tree

Generated from **155 tracked files** in GitHub `main`. This is an index of real project files, not evidence of public-safety certification or live hosting.

```text
CivicShield-AI/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   └── feature_request.yml
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── model-validation.yml
│   │   └── pages.yml
│   └── dependabot.yml
├── artifacts/
│   ├── evaluation_reports/
│   │   └── .gitkeep
│   └── models/
│       └── .gitkeep
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── geo_query.py
│   │   ├── main.py
│   │   ├── oidc.py
│   │   ├── reviewer_identity.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── migrations/
│   │   ├── versions/
│   │   │   ├── 20261026_0001_initial.py
│   │   │   └── 20261028_0002_reviewer_actor.py
│   │   ├── env.py
│   │   ├── postgis_indexes.sql
│   │   └── script.py.mako
│   ├── __init__.py
│   └── Dockerfile
├── data/
│   ├── processed/
│   │   └── .gitkeep
│   ├── raw/
│   │   └── .gitkeep
│   └── README.md
├── docs/
│   ├── assets/
│   │   ├── architecture-overview.svg
│   │   ├── architecture.svg
│   │   ├── dashboard-concept.svg
│   │   ├── hero-banner.svg
│   │   ├── incident-workflow.svg
│   │   ├── ml-evaluation-flow.svg
│   │   ├── risk-thresholds.svg
│   │   └── source-provenance.svg
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── BROWSER_ACCEPTANCE.md
│   ├── CASE_STUDY.md
│   ├── DATA_SOURCES.md
│   ├── DEMO_SCRIPT.md
│   ├── DEPLOYMENT.md
│   ├── END_TO_END_VERIFICATION.md
│   ├── GITHUB_PAGES_PUBLISH.md
│   ├── IMD_CWC_INTEGRATION.md
│   ├── MODEL_CARD.md
│   ├── OPERATIONS.md
│   ├── PRODUCTION_SETUP.md
│   ├── PROJECT_TREE.md
│   ├── PROJECT_WORKFLOW.md
│   ├── QUICKSTART_WINDOWS.md
│   ├── RELEASE_CHECKLIST.md
│   ├── RELEASE_STATUS.md
│   ├── ROADMAP.md
│   ├── SAFETY_AND_PRIVACY.md
│   ├── TEST_PLAN.md
│   └── VISUALIZATIONS.md
├── frontend/
│   ├── e2e/
│   │   └── portfolio.spec.js
│   ├── src/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── auth.js
│   │   ├── Diagnostics.jsx
│   │   ├── KnowledgeSearch.jsx
│   │   ├── LiveWeather.jsx
│   │   ├── main.jsx
│   │   ├── MapPanel.jsx
│   │   ├── OfficialSources.jsx
│   │   ├── ScenarioLab.jsx
│   │   ├── styles-extra.css
│   │   └── styles.css
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   ├── package.json
│   ├── playwright.config.js
│   └── vite.config.js
├── scripts/
│   ├── __init__.py
│   ├── backup_sqlite.py
│   ├── check_data_quality.py
│   ├── collect_weather.py
│   ├── doctor.py
│   ├── plot_metrics.py
│   ├── purge_incidents.py
│   ├── smoke_compose.py
│   ├── smoke_demo.py
│   ├── start-local.ps1
│   ├── stop-local.ps1
│   ├── verify_postgis.py
│   └── verify_site.py
├── site/
│   ├── assets/
│   │   ├── architecture-overview.svg
│   │   ├── dashboard-concept.svg
│   │   ├── hero-banner.svg
│   │   ├── ml-evaluation-flow.svg
│   │   └── source-provenance.svg
│   ├── favicon.svg
│   ├── index.html
│   └── robots.txt
├── src/
│   └── civicshield/
│       ├── assistant/
│       │   ├── __init__.py
│       │   ├── guidance.py
│       │   └── retrieval.py
│       ├── data_processing/
│       │   ├── __init__.py
│       │   └── features.py
│       ├── demo/
│       │   ├── __init__.py
│       │   └── scenarios.py
│       ├── incident_management/
│       │   ├── __init__.py
│       │   ├── geospatial.py
│       │   └── triage.py
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── cwc_official.py
│       │   ├── imd_official.py
│       │   ├── open_meteo.py
│       │   └── sources.py
│       ├── ml/
│       │   ├── __init__.py
│       │   ├── experiment.py
│       │   ├── explain.py
│       │   ├── predict.py
│       │   ├── train.py
│       │   └── validate_external.py
│       ├── monitoring/
│       │   ├── __init__.py
│       │   ├── drift.py
│       │   └── freshness.py
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_compose_smoke.py
│   ├── test_deployment_doctor.py
│   ├── test_geospatial_search.py
│   ├── test_guidance.py
│   ├── test_integrations.py
│   ├── test_new_features.py
│   ├── test_operations.py
│   ├── test_readiness.py
│   ├── test_release_integrity.py
│   ├── test_repository_hygiene.py
│   ├── test_risk.py
│   ├── test_scenario_lab.py
│   ├── test_smoke_demo.py
│   ├── test_static_portfolio.py
│   ├── test_training.py
│   ├── test_visual_assets.py
│   └── test_visualizations.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
├── render.yaml
└── SECURITY.md
```

## Essential links

- [Full-stack engineering architecture](ARCHITECTURE.md) and [visual gallery](VISUALIZATIONS.md)
- [React UI, keyboard navigation and Playwright tests](BROWSER_ACCEPTANCE.md)
- [Local Docker Compose and PostgreSQL/PostGIS integration](END_TO_END_VERIFICATION.md)
- [Interactive fabricated case study](CASE_STUDY.md)
- [Static GitHub Pages publishing guide](GITHUB_PAGES_PUBLISH.md)
- [Complete release status and unresolved external dependencies](RELEASE_STATUS.md)
- [Windows quick start](QUICKSTART_WINDOWS.md) and [deployment controls](PRODUCTION_SETUP.md)

No real IMD/CWC authority, hosted identity-provider tenant, validated flood predictions, or government emergency operations are asserted.
