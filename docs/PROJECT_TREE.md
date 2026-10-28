# CivicShield AI — live GitHub project tree

This diagram was regenerated from **144 tracked source files** in the `main` branch. A source tree is not evidence of real emergency-service certification.

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
│   ├── CASE_STUDY.md
│   ├── DATA_SOURCES.md
│   ├── DEMO_SCRIPT.md
│   ├── DEPLOYMENT.md
│   ├── END_TO_END_VERIFICATION.md
│   ├── IMD_CWC_INTEGRATION.md
│   ├── MODEL_CARD.md
│   ├── OPERATIONS.md
│   ├── PRODUCTION_SETUP.md
│   ├── PROJECT_TREE.md
│   ├── PROJECT_WORKFLOW.md
│   ├── QUICKSTART_WINDOWS.md
│   ├── RELEASE_CHECKLIST.md
│   ├── ROADMAP.md
│   ├── SAFETY_AND_PRIVACY.md
│   ├── TEST_PLAN.md
│   └── VISUALIZATIONS.md
├── frontend/
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
│   └── verify_postgis.py
├── site/
│   ├── assets/
│   │   ├── architecture-overview.svg
│   │   ├── dashboard-concept.svg
│   │   └── hero-banner.svg
│   └── index.html
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

## Main areas

- [React dashboard and fictional Scenario Lab](../frontend/src/)
- [Backend routes, health and OIDC reviewer access](../backend/app/)
- [Pure offline case-study generator](../src/civicshield/demo/scenarios.py)
- [Source provenance and ML experiments](../src/civicshield/)
- [Database migrations and optional PostGIS index](../backend/migrations/)
- [Full Docker Compose Nginx/API/database acceptance](END_TO_END_VERIFICATION.md)
- [Static portfolio visuals](VISUALIZATIONS.md)
- [Windows setup](QUICKSTART_WINDOWS.md)
- [Production security and readiness checklist](PRODUCTION_SETUP.md)
- [Official source access and scientific validation boundaries](ROADMAP.md)

No live government warning API is guaranteed; public operational use is not authorized.
