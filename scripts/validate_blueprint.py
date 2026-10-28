"""Offline Render Blueprint safety and deployability sanity checks.

This checker catches local configuration mistakes. It cannot validate a Render
account, actual provider permissions, DNS, OIDC tenants, billing or live feeds.
"""
from __future__ import annotations
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "render.yaml"

def validate_blueprint(content: str) -> dict:
    config = yaml.safe_load(content)
    if not isinstance(config, dict):
        raise ValueError("Expected a Render Blueprint YAML mapping")
    databases = config.get("databases", [])
    services = config.get("services", [])
    if len(databases) != 1 or len(services) != 2:
        raise ValueError("Blueprint must contain one database, API and static frontend")

    db = databases[0]
    # Render's modern compute plan IDs have replaced ambiguous legacy labels.
    if not re.fullmatch(r"(?:free|[0-9]+(?:\.[0-9]+)?c-[0-9]+(?:mb|g))", str(db.get("plan", ""))):
        raise ValueError("Unsupported or ambiguous PostgreSQL compute plan label")
    if db.get("ipAllowList") != []:
        raise ValueError("Database must not permit direct internet addresses")
    api = next((s for s in services if s.get("name") == "civicshield-api"), None)
    frontend = next((s for s in services if s.get("name") == "civicshield-web"), None)
    if not api or not frontend:
        raise ValueError("Required API and frontend services are missing")
    if (api.get("type"), api.get("runtime")) != ("web", "docker"):
        raise ValueError("API must be an explicit Docker web service")
    if api.get("dockerfilePath") != "./backend/Dockerfile" or api.get("dockerContext") != ".":
        raise ValueError("API image build paths are not aligned with the monorepo")
    if api.get("healthCheckPath") != "/api/ready":
        raise ValueError("API must use DB/schema readiness endpoint")
    if api.get("preDeployCommand") != "python -m alembic upgrade head":
        raise ValueError("Database migrations must run before a new API deployment")
    if api.get("autoDeployTrigger") != "off":
        raise ValueError("Public API deploys require deliberate manual approval")

    if (frontend.get("type"), frontend.get("runtime")) != ("web", "static"):
        raise ValueError("Frontend must be a static Render site")
    if frontend.get("rootDir") != "frontend" or frontend.get("staticPublishPath") not in ("dist", "./dist"):
        raise ValueError("Static frontend build path is not configured")
    if frontend.get("autoDeployTrigger") != "off":
        raise ValueError("Frontend deploys should not be automatically triggered")
    routes = frontend.get("routes", [])
    if not any(r.get("type") == "rewrite" and r.get("source") == "/*"
               and r.get("destination") == "/index.html" for r in routes):
        raise ValueError("React SPA refresh requires a catch-all index.html rewrite")

    api_vars = {v["key"]: v for v in api.get("envVars", [])}
    web_vars = {v["key"]: v for v in frontend.get("envVars", [])}
    for key, expected in (
        ("APP_ENV", "production"), ("AUTH_MODE", "oidc"),
        ("INCIDENT_SUBMISSIONS_ENABLED", "false"),
        ("IMD_API_ENABLED", "false"), ("OPEN_METEO_ENABLED", "false"),
    ):
        if str(api_vars.get(key, {}).get("value", "")).lower() != expected:
            raise ValueError(f"API setting {key} must be fail-closed by default")
    if api_vars.get("DATABASE_URL", {}).get("fromDatabase", {}).get("name") != db.get("name"):
        raise ValueError("API must use the declared managed PostgreSQL database")
    for key in ("OIDC_ISSUER", "OIDC_AUDIENCE", "OIDC_JWKS_URL", "CORS_ORIGINS"):
        if api_vars.get(key, {}).get("sync") is not False:
            raise ValueError(f"Missing operator-provisioned setting: {key}")
    if api_vars.get("AUDIT_HASH_SECRET", {}).get("generateValue") is not True:
        raise ValueError("Audit key must be created by the secret manager")
    for key in ("VITE_API_BASE", "VITE_OIDC_AUTHORITY", "VITE_OIDC_CLIENT_ID", "VITE_OIDC_SCOPE"):
        if web_vars.get(key, {}).get("sync") is not False:
            raise ValueError(f"Missing operator-provisioned build-time setting: {key}")
    if str(web_vars.get("VITE_AUTH_MODE", {}).get("value")) != "oidc":
        raise ValueError("Public frontend must use OIDC")
    headers = {(h.get("path"), h.get("name")): h.get("value") for h in frontend.get("headers", [])}
    if headers.get(("/*", "X-Content-Type-Options")) != "nosniff":
        raise ValueError("Static site must disable content sniffing")
    if headers.get(("/*", "X-Frame-Options")) != "DENY":
        raise ValueError("Static site must refuse framing")
    return {
        "result": "blueprint_configuration_verified",
        "components": ["managed_postgres", "docker_api", "react_static_site"],
        "external_account_connected": False,
        "external_idp_validated": False,
        "real_world_emergency_service": False,
        "message": "Configuration audit only. This may incur provider charges if deployed.",
    }

def main() -> int:
    try:
        result = validate_blueprint(SOURCE.read_text(encoding="utf-8"))
    except (ValueError, OSError, yaml.YAMLError, KeyError, TypeError) as e:
        print(f"Render Blueprint audit FAILED: {e}", file=sys.stderr)
        return 1
    print(result)
    return 0

if __name__ == "__main__":
    sys.exit(main())
