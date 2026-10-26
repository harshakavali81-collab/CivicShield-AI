# Actual repository tree

~~~text
CivicShield-AI/
├── .env.example
├── .gitignore
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       └── model-validation.yml
├── backend/
│   ├── __init__.py
│   ├── Dockerfile
│   └── app/
│       ├── __init__.py
│       ├── config.py
│       ├── db.py
│       ├── main.py
│       └── schemas.py
├── src/civicshield/
│   ├── __init__.py
│   ├── assistant/
│   │   ├── __init__.py
│   │   └── guidance.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── features.py
│   ├── incident_management/
│   │   ├── __init__.py
│   │   └── triage.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── sources.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── train.py
│   └── monitoring/
│       ├── __init__.py
│       └── freshness.py
├── frontend/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── MapPanel.jsx
│       ├── api.js
│       └── styles.css
├── artifacts/
│   ├── models/.gitkeep
│   └── evaluation_reports/.gitkeep
├── data/
│   ├── README.md
│   ├── raw/.gitkeep
│   └── processed/.gitkeep
├── scripts/
│   ├── __init__.py
│   └── plot_metrics.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_guidance.py
│   ├── test_risk.py
│   ├── test_training.py
│   └── test_visualizations.py
├── docs/
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── DATA_SOURCES.md
│   ├── DEMO_SCRIPT.md
│   ├── DEPLOYMENT.md
│   ├── MODEL_CARD.md
│   ├── PROJECT_TREE.md
│   ├── PROJECT_WORKFLOW.md
│   ├── ROADMAP.md
│   ├── SAFETY_AND_PRIVACY.md
│   ├── TEST_PLAN.md
│   ├── VISUALIZATIONS.md
│   └── assets/
│       └── architecture.svg
├── docker-compose.yml
├── LICENSE
├── Makefile
├── pyproject.toml
└── README.md
~~~

## Folder explanations

| Folder | Purpose |
| --- | --- |
| \`backend/app\` | Versioned HTTP API, validation, SQL storage and reviewer controls |
| \`src/civicshield/ml\` | Temporal supervised experiment and opt-in scoring |
| \`src/civicshield/assistant\` | Embedded five-language education summaries |
| \`src/civicshield/ingestion\` | Official link catalog, not a live integration |
| \`src/civicshield/incident_management\` | Privacy redaction, classification, duplicate flagging |
| \`src/civicshield/monitoring\` | Source freshness guard; no production telemetry yet |
| \`frontend\` | React dashboard, map, charts, forms |
| \`data\` | Local ignored user datasets and schema policy |
| \`artifacts\` | Ignored trained models; do not commit user model binaries |
| \`docs\` | Explanations, architecture and limitations |
| \`tests\` | Safety, API and ML assertions |

The README and architecture files render GitHub Mermaid diagrams as graphs.
