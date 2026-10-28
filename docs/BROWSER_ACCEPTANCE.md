# Browser acceptance tests — real Chromium and integrated Docker stack

The portfolio UI is now exercised through **real browser interactions**, not just a JavaScript compilation check.

## What CI runs

GitHub Actions starts PostgreSQL/PostGIS, FastAPI, Nginx and the compiled React dashboard with `docker compose up -d --build --wait`. It runs a zero-dependency HTTP smoke test, then installs Playwright + Chromium and executes the browser tests in `frontend/e2e/portfolio.spec.js`.

The five browser tests verify:

1. Dashboard loads and its **NOT LIVE** label stays visible. The fictional Scenario Lab renders a two-series graph and four interactive engineering walkthrough stages.
2. The risk explorer **refuses stale input**. A seven-hour-old demo input returns `unavailable` and an explicit experimental-safety warning.
3. Official source connections remain disconnected without authorized access, and the IMD bulletin request button is disabled.
4. Mobile navigation opens and closes; Escape dismisses it and choosing a page restores focus to the main content.
5. The keyboard-accessible **Skip to main content** link moves focus to the content landmark.

Browser tests do **not** prove actual government authorization, a real public deployment, scientific model validity or emergency response capability.

## Run locally

Start the full application using Docker Desktop or Docker Compose, then run:

```bash
cd frontend
npm install --no-audit --no-fund
npx playwright install chromium
npm run test:e2e
```

Default test base: `http://127.0.0.1:5173`. Override with `E2E_BASE_URL` in your own controlled environment. CI uses a disposable database and disables incident submissions and live modeled weather.

On browser failure CI uploads screenshots and traces as a temporary test artifact (without incident data); never attach real user reports to browser tests.

## Accessibility improvements

Navigation now includes a skip link, an accessible `main` landmark, `aria-current` for the active page, explicit mobile menu expansion status, Escape-to-close behavior, visible keyboard focus and reduced-motion support.

These improvements **do not** constitute a WCAG 2.2 audit, screen-reader field study or native-language translation review.
