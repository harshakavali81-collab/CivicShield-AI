# 🛡️ CivicShield AI

**Multilingual Public Safety, Disaster Risk Demonstration & Incident Review Platform**

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Concept dashboard layout](<docs/assets/dashboard-concept.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.


> **Visual integrity:** These SVGs are original **concept illustrations and technical diagrams**, not screenshots of a deployed production service. This is **not an official warning** platform; no images claim real hazard predictions, operational coverage, or validated model accuracy.

| Application concept | Architecture and data flow |
| :---: | :---: |
| [![Concept dashboard layout](docs/assets/dashboard-concept.svg)](docs/assets/dashboard-concept.svg) | [![System architecture overview](docs/assets/architecture-overview.svg)](docs/assets/architecture-overview.svg) |
| **[Concept dashboard](docs/assets/dashboard-concept.svg)** · example interface and illustrative data | **[System architecture](docs/assets/architecture-overview.svg)** · trust boundaries and components |

| Human report review | Experimental ML flow |
| :---: | :---: |
| [![Incident moderation workflow](docs/assets/incident-workflow.svg)](docs/assets/incident-workflow.svg) | [![Model research evaluation process](docs/assets/ml-evaluation-flow.svg)](docs/assets/ml-evaluation-flow.svg) |
| **[Incident workflow](docs/assets/incident-workflow.svg)** · review decisions remain human | **[ML evaluation](docs/assets/ml-evaluation-flow.svg)** · no operational accuracy claims |

| Source provenance | Demonstration thresholds |
| :---: | :---: |
| [![Official provider status and provenance](docs/assets/source-provenance.svg)](docs/assets/source-provenance.svg) | [![Illustrative rainfall groupings](docs/assets/risk-thresholds.svg)](docs/assets/risk-thresholds.svg) |
| **[Source attribution](docs/assets/source-provenance.svg)** · disconnected ≠ safe | **[Risk thresholds](docs/assets/risk-thresholds.svg)** · not official warning levels |

[Browse the complete visual gallery](docs/VISUALIZATIONS.md) · [Architecture](docs/ARCHITECTURE.md) · [Actual project tree](docs/PROJECT_TREE.md)


The fictional scenario lab supports exploration of demonstration inputs; it is not an official warning or emergency service.

## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

- **Risk explorer:** explicit, explainable demonstration thresholds; stale inputs are rejected. Optionally use a user-trained supervised model based on legally obtained labeled historical data.
- **Multilingual guidance:** English, Telugu, Hindi, Tamil and Kannada curated preparedness responses; separate searchable source-linked mini library. Not an LLM-based, live official RAG service.
- **Citizen incident reports:** input validation, privacy-conscious storage, duplicate detection, suggested priority and **human-only** review decisions.
- **Responsive React dashboard:** map, incident analytics, actual locally submitted report-count trends, and clearly labeled demo locations. Opt-in provider-backed weather explorer with source attribution.
- **Developer quality:** FastAPI, SQLAlchemy (SQLite local / PostgreSQL for Docker), Alembic initial migration, controlled backups/purge, tests, Docker Compose, CI, architecture diagrams, docs, local experiment graph generator.
- **Safety:** no invented government alerts, no personal phone collection, no public disclosure of exact incident coordinates or narratives, reviewer audit log and optional reporter key. No distributed RBAC/anti-abuse claims.

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/CivicShield-AI.git
cd CivicShield-AI
```

### API (Python 3.11+)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev,migrations]"
uvicorn backend.app.main:app --reload
pytest -q
```

Open http://localhost:8000/docs. The local database defaults to SQLite.

### Web dashboard (Node 20+)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/api` to the FastAPI backend.

### Docker

```bash
cp .env.example .env
docker compose up --build
```

Docker provides PostGIS/PostgreSQL as persistence. Local development is bound to localhost only. Set a strong local `POSTGRES_PASSWORD` in `.env`. Incident submissions are disabled by default in the API unless explicitly enabled. Set a strong `RESPONDER_API_KEY` to enable authenticated review routes. **Do not deploy this configuration to the public internet.**

## Challenges & Solutions

**Repository organization:** this project uses `src/`, `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

This repository provides a locally runnable **demonstration**, not a deployed production emergency service. Live IMD warning feeds, validated forecasting datasets, a genuine generative retrieval-augmented assistant, calibrated models, government integrations, production OIDC/RBAC, distributed anti-abuse controls, accessibility field tests and production monitoring require additional engineering or approvals. Optional SHAP/MLflow code is experimental and not deployed. See [roadmap](docs/ROADMAP.md).

## Scope and supporting evidence

<p align="center">
  <img src="docs/assets/hero-banner.svg" width="100%" alt="CivicShield AI illustrated research dashboard banner. Concept artwork, not a live emergency warning service.">
</p>

<p align="center">
  <a href="https://github.com/harshakavali81-collab/CivicShield-AI/actions/workflows/ci.yml"><img src="https://github.com/harshakavali81-collab/CivicShield-AI/actions/workflows/ci.yml/badge.svg" alt="Continuous integration status"></a>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB" alt="Python 3.11 or newer">
  <img src="https://img.shields.io/badge/Frontend-React-61DAFB" alt="React">
  <img src="https://img.shields.io/badge/License-MIT-56C3AE" alt="MIT licensed">
  <img src="https://img.shields.io/badge/Scope-Research%20Demo-F1AD62" alt="Research demo, not certified">
</p>

**Multilingual Public Safety, Disaster Risk Demonstration & Incident Review Platform**

[Architecture](docs/ARCHITECTURE.md) · [Project tree](docs/PROJECT_TREE.md) · [Workflow](docs/PROJECT_WORKFLOW.md) · [API](docs/API_REFERENCE.md) · [Model card](docs/MODEL_CARD.md) · [Safety and privacy](docs/SAFETY_AND_PRIVACY.md) · [Testing](docs/TEST_PLAN.md) · [Visualizations](docs/VISUALIZATIONS.md) · [Deployment](docs/DEPLOYMENT.md) · [Operations](docs/OPERATIONS.md) · [Roadmap](docs/ROADMAP.md)

> **SAFETY NOTICE:** This is a portfolio/research demo, **not** an official warning system, emergency service, evacuation tool, or reliable prediction of disaster safety. Risk indicators are experimental; demo samples are synthetic. Follow official authorities. During emergencies contact local emergency services.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/CivicShield-AI/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

See [LICENSE](LICENSE) for the existing terms.
