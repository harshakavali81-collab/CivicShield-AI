# Publish CivicShield AI's informational portfolio using GitHub Pages

The **site/** directory contains a responsive HTML/CSS research-portfolio page and original SVG illustrations. It is not the React/FastAPI application or a live emergency warning service.

## What is included

- `site/index.html`: static portfolio, explicit research-only description, a fictional case study and keyboard skip link.
- `site/assets/`: original SVG diagrams that are checked against local references.
- `site/favicon.svg` and `site/robots.txt`: project identity and crawler instructions.
- `scripts/verify_site.py`: offline check for valid assets, accessible image descriptions and accurate fictional-data disclaimer.
- `.github/workflows/pages.yml`: manually triggered publishing workflow with validation.

## Owner action needed for a public website

1. Open [CivicShield AI repository Pages settings](https://github.com/harshakavali81-collab/CivicShield-AI/settings/pages).
2. Under **Build and deployment**, set **Source: GitHub Actions**.
3. Open [Publish static portfolio workflow](https://github.com/harshakavali81-collab/CivicShield-AI/actions/workflows/pages.yml), select **Run workflow**, choose main and run it.
4. Verify the deployment job succeeds, then copy the **actual published URL** from GitHub's Pages output. Do not claim an unverified public URL.

If deployment fails, use the workflow logs and ensure Pages permissions and the github-pages environment are enabled. This does not create DNS records or custom domains.

## Limits

GitHub Pages serves static files only. It does not operate FastAPI, OIDC authentication, PostgreSQL, official IMD/CWC APIs, real-time incident reporting or model inference. A hosted dynamic stack requires a cloud account, secure secrets and independent review. The validated static site makes no operational emergency-service claims.
