# CivicShield AI — complete GitHub project tree

Generated from **160 tracked source files** on the current `main` branch. All files below exist in the repository. This structure does not prove real-world hazard prediction or operational emergency-service certification.

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
│   ├── RENDER_BLUEPRINT_GUIDE.md
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
│   ├── package_portfolio.py
│   ├── plot_metrics.py
│   ├── purge_incidents.py
│   ├── smoke_compose.py
│   ├── smoke_demo.py
│   ├── start-local.ps1
│   ├── stop-local.ps1
│   ├── validate_blueprint.py
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
│   ├── test_portfolio_package.py
│   ├── test_readiness.py
│   ├── test_release_integrity.py
│   ├── test_render_blueprint.py
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

## Engineering and portfolio entry points

- [Project overview, how to run and visual gallery](../README.md)
- [Case-study diagrams and research walkthrough](CASE_STUDY.md)
- [Full local API, database, React and Nginx integration](END_TO_END_VERIFICATION.md)
- [Chromium browser interaction and accessibility tests](BROWSER_ACCEPTANCE.md)
- [Render cloud Blueprint guards and explicit account/cost requirements](RENDER_BLUEPRINT_GUIDE.md)
- [Reproducible offline static portfolio ZIP generator](../scripts/package_portfolio.py)
- [Static informational GitHub Pages deployment checklist](GITHUB_PAGES_PUBLISH.md)
- [Source/code/release CI jobs](../.github/workflows/ci.yml)
- [Exact remaining external dependencies](RELEASE_STATUS.md)

**Scope notice:** Cloud hosting, real identity providers, official IMD/CWC permissions and independently certified disaster prediction remain outside this verified code release.
