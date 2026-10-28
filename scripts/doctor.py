"""Offline deployment preflight; checks configurations without printing secret values.

Examples:
  python -m scripts.doctor --mode local
  python -m scripts.doctor --mode production
  python -m scripts.doctor --mode production --json
The preflight cannot prove a cloud account, government permission or model accuracy.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
from urllib.parse import urlsplit

CHECKS = {
    "APP_ENV": "runtime environment",
    "DATABASE_URL": "database connection string",
    "AUTH_MODE": "authentication mode",
    "OIDC_ISSUER": "trusted IdP issuer",
    "OIDC_AUDIENCE": "API audience",
    "OIDC_JWKS_URL": "IdP JWKS endpoint",
    "CORS_ORIGINS": "allowed dashboard domains",
    "AUDIT_HASH_SECRET": "audit pseudonym key",
}

def _https_host(url: str) -> bool:
    try:
        u = urlsplit(url)
    except ValueError:
        return False
    return (u.scheme == "https" and bool(u.netloc) and
            u.hostname not in ("localhost", "127.0.0.1") and
            not u.username and not u.password and not u.fragment)

def _https_origin(url: str) -> bool:
    try:
        u = urlsplit(url)
    except ValueError:
        return False
    return (_https_host(url) and u.path in ("", "/") and not u.query)

def evaluate(mode: str = "local", env: dict | None = None, executable=shutil.which) -> dict:
    if mode not in ("local", "production"):
        raise ValueError("mode must be 'local' or 'production'")
    config = dict(os.environ if env is None else env)
    failures, advisories, checks = [], [], []
    is_production = mode == "production"

    if executable("python") is None and executable("python3") is None:
        advisories.append("Python command not detected on PATH; verify Python >=3.11.")
    else:
        checks.append("Python executable detected")

    if not is_production:
        if executable("docker") is None:
            advisories.append("Docker is optional; install Docker for the one-command Compose demo.")
        else:
            checks.append("Docker executable detected")
        if not executable("node"):
            advisories.append("Node is optional for source-based React development.")
        if config.get("INCIDENT_SUBMISSIONS_ENABLED", "false").lower() == "true":
            advisories.append("Demo incident intake is enabled; use only artificial test reports.")
        if not config.get("POSTGRES_PASSWORD"):
            advisories.append("Set POSTGRES_PASSWORD in your gitignored .env before Docker Compose.")
        if config.get("IMD_API_ENABLED", "false").lower() == "true":
            advisories.append("IMD adapter flag is enabled; verify approved access and permissions separately.")
    else:
        if config.get("APP_ENV") != "production":
            failures.append("APP_ENV must be production.")
        if config.get("AUTH_MODE", "").lower() != "oidc":
            failures.append("AUTH_MODE must be oidc.")
        db_url = config.get("DATABASE_URL", "")
        if not db_url.startswith(("postgresql://", "postgresql+psycopg://")):
            failures.append("DATABASE_URL must use a managed PostgreSQL connection.")
        if config.get("INCIDENT_SUBMISSIONS_ENABLED", "false").lower() == "true":
            failures.append("Public citizen intake must remain disabled until an independent safety and privacy review.")
        for field in ("OIDC_ISSUER", "OIDC_JWKS_URL"):
            if not _https_host(config.get(field, "")):
                failures.append(f"{field} must be an external HTTPS URL.")
        if not config.get("OIDC_AUDIENCE"):
            failures.append("OIDC_AUDIENCE is missing.")
        origins = [o.strip() for o in config.get("CORS_ORIGINS", "").split(",") if o.strip()]
        if not origins or not all(_https_origin(o) and "*" not in o for o in origins):
            failures.append("CORS_ORIGINS must list explicit external HTTPS origins.")
        if len(config.get("AUDIT_HASH_SECRET", "")) < 32:
            failures.append("AUDIT_HASH_SECRET must contain at least 32 private characters.")
        if config.get("IMD_API_ENABLED", "false").lower() == "true":
            advisories.append("IMD API enabled flag does NOT certify approval, authentication, or valid observations.")
        checks.append("Configuration only: no cloud, data-rights, login or disaster-model validation performed.")
    return {
        "mode": mode, "configuration_pass": not failures, "errors": failures,
        "advisories": advisories, "checks": checks,
        "real_identity_provider_verified": False,
        "live_cloud_deployment_verified": False,
        "official_hazard_feed_verified": False,
        "scientific_prediction_validated": False,
        "note": "No secrets, full connection strings or personal account information are printed.",
    }

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=["local", "production"], default="local")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    result = evaluate(args.mode)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Configuration check: {'PASS' if result['configuration_pass'] else 'BLOCKED'} ({args.mode})")
        for line in result["errors"]:
            print(f"BLOCKER: {line}")
        for line in result["advisories"]:
            print(f"NOTE: {line}")
        print("This check does not certify official feeds, model quality, cloud deployment or emergency readiness.")
    if not result["configuration_pass"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
