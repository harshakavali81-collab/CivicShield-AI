# CivicShield AI — complete tracked source tree

Generated from the 122 tracked files on the GitHub `main` branch. The tree below is source structure, not certification of public emergency safety or official integrations.

```text
CivicShield-AI/
├── .github/
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
│   ├── DATA_SOURCES.md
│   ├── DEMO_SCRIPT.md
│   ├── DEPLOYMENT.md
│   ├── IMD_CWC_INTEGRATION.md
│   ├── MODEL_CARD.md
│   ├── OPERATIONS.md
│   ├── PRODUCTION_SETUP.md
│   ├── PROJECT_TREE.md
│   ├── PROJECT_WORKFLOW.md
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
│   ├── plot_metrics.py
│   ├── purge_incidents.py
│   ├── smoke_demo.py
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
│   ├── test_geospatial_search.py
│   ├── test_guidance.py
│   ├── test_integrations.py
│   ├── test_new_features.py
│   ├── test_operations.py
│   ├── test_readiness.py
│   ├── test_risk.py
│   ├── test_smoke_demo.py
│   ├── test_training.py
│   ├── test_visual_assets.py
│   └── test_visualizations.py
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
└── render.yaml
```

## Engineering entry points

- [API, auth, and readiness](../backend/app/main.py)
- [Optional indexed PostGIS spatial search](../backend/app/geo_query.py)
- [OIDC reviewer identity and pseudonymous audits](../backend/app/oidc.py)
- [Initial and review-audit migrations](../backend/migrations/versions/)
- [Independent model evaluation](../src/civicshield/ml/validate_external.py)
- [React dashboards and diagnostics](../frontend/src/)
- [PostgreSQL/PostGIS integration CI](../.github/workflows/ci.yml)
- [Read-only end-to-end demo smoke CLI](../scripts/smoke_demo.py)
- [Visual gallery and diagrams](VISUALIZATIONS.md)
- [Operations/deployment](OPERATIONS.md) · [Production setup](PRODUCTION_SETUP.md) · [Remaining dependencies](ROADMAP.md)

**Research only:** official IMD/CWC access, validated hazard predictions, approved emergency response, and public deployment are not implied.
