# CivicShield AI — actual Chromium browser screenshots

The repository has original SVG project concept artwork under `docs/assets/`, but those drawings are **not** live-app screenshots.

GitHub CI now separately runs the actual integrated FastAPI + PostgreSQL/PostGIS + Nginx/React application and uses Playwright Chromium to create these four honest snapshots:

| Output | What it demonstrates |
| --- | --- |
| `01-desktop-dashboard.png` | Full-width research dashboard with NOT LIVE notice |
| `02-fictional-scenario-lab.png` | Interactive charts from invented canonical sample data |
| `03-disconnected-official-sources.png` | Official source connection status and unavailable live feeds |
| `04-mobile-dashboard.png` | Responsive narrow-screen dashboard |

These **browser-tested screenshots** are generated automatically from a disposable database. They are intended as portfolio evidence of visual software functionality—not evidence of live weather data, scientific risk-prediction accuracy, public hosting, government approval, or a real incident operation.

## Download the screenshots

1. Open [GitHub Actions — CI workflow](https://github.com/harshakavali81-collab/CivicShield-AI/actions/workflows/ci.yml).
2. Choose a **successful** run on the latest main commit.
3. Under **Artifacts**, download `civicshield-tested-ui-screenshots`.
4. Extract the ZIP and view the four PNGs. The artifact is retained for 30 days.

Only the generated test screenshots are in this artifact; no user report content, real API keys, access tokens or private identities are placed in screenshots. There is no claim that these images were taken from a public production deployment.

## Generate them locally

After starting the Docker demo at `http://127.0.0.1:5173`:

```bash
cd frontend
npm install
npx playwright install chromium
npx playwright test e2e/screenshots.spec.js
```

Images appear under `frontend/test-results/showcase`. Use artificial empty/local demo data only. Do **not** generate screenshots from a database containing actual personal reports.
