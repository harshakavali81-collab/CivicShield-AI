# CivicShield AI — live repository tree

Generated from the actual tracked GitHub tree of the project's \`main\` branch. It may evolve as commits land.

~~~text
CivicShield-AI/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── model-validation.yml
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
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── migrations/
│   │   ├── versions/
│   │   │   └── 20261026_0001_initial.py
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
│   │   └── architecture.svg
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── DATA_SOURCES.md
│   ├── DEMO_SCRIPT.md
│   ├── DEPLOYMENT.md
│   ├── MODEL_CARD.md
│   ├── OPERATIONS.md
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
│   │   ├── KnowledgeSearch.jsx
│   │   ├── LiveWeather.jsx
│   │   ├── main.jsx
│   │   ├── MapPanel.jsx
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
│   └── purge_incidents.py
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
│       │   ├── open_meteo.py
│       │   └── sources.py
│       ├── ml/
│       │   ├── __init__.py
│       │   ├── experiment.py
│       │   ├── explain.py
│       │   ├── predict.py
│       │   └── train.py
│       ├── monitoring/
│       │   ├── __init__.py
│       │   ├── drift.py
│       │   └── freshness.py
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_guidance.py
│   ├── test_new_features.py
│   ├── test_operations.py
│   ├── test_risk.py
│   ├── test_training.py
│   └── test_visualizations.py
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── LICENSE
├── Makefile
├── pyproject.toml
└── README.md
~~~

## Component summary

| Directory | Responsibilities |
| --- | --- |
| \`backend/app\` | FastAPI routing, Pydantic, DB entities, security and human review |
| \`backend/migrations\` | Initial Alembic schema revision; optional manual PostGIS index |
| \`src/civicshield/ingestion\` | Open-Meteo modeled-weather client and official-bookmark catalog |
| \`src/civicshield/ml\` | Binary supervised research training, experimental risk scoring and optional SHAP/MLflow |
| \`src/civicshield/assistant\` | Curated multilingual preparedness answers and manual-source lexical retrieval |
| \`src/civicshield/incident_management\` | Text triage, duplicate fingerprints and distance calculation |
| \`src/civicshield/data_processing\` | Shared ML feature schema |
| \`src/civicshield/monitoring\` | Source freshness and illustrative drift computation |
| \`frontend\` | React/Vite dashboard, Leaflet map, provider weather, incident forms, charts |
| \`tests\` | API, ML, safety, provider, operations and migration/backup-related assertions |
| \`scripts\` | Dataset auditing, weather collection, local backup/retention and SVG graphs |
| \`data\` | Untracked/ignored local observations only |
| \`artifacts\` | Untracked/ignored model and evaluation outputs |
| \`docs\` | Full project explanation, architecture/sequence diagrams, model card and setup |
| \`.github/workflows\` | Backend tests, frontend build and migration smoke checks |

[Architecture](ARCHITECTURE.md) · [Workflow](PROJECT_WORKFLOW.md) · [Visualizations](VISUALIZATIONS.md) · [Operational runbook](OPERATIONS.md) · [Roadmap](ROADMAP.md)

**Reminder:** The complete folder tree does not imply real-world emergency-readiness.
