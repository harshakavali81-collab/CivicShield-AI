"""Catch cloud blueprint drift without claiming a real Render account exists."""
from copy import deepcopy
from pathlib import Path
import yaml
import pytest
from scripts.validate_blueprint import validate_blueprint

SOURCE = (Path(__file__).resolve().parents[1] / "render.yaml").read_text("utf-8")

def test_verified_blueprint_is_explicitly_not_deployed():
    result = validate_blueprint(SOURCE)
    assert result["result"] == "blueprint_configuration_verified"
    assert result["external_account_connected"] is False
    assert result["external_idp_validated"] is False

@pytest.mark.parametrize("mutation", [
    lambda cfg: cfg["databases"][0].update(plan="basic"),
    lambda cfg: cfg["databases"][0].update(ipAllowList=["0.0.0.0/0"]),
    lambda cfg: cfg["services"][0].update(preDeployCommand="true"),
    lambda cfg: cfg["services"][0].update(autoDeployTrigger="commit"),
    lambda cfg: cfg["services"][1].update(routes=[]),
    lambda cfg: cfg["services"][1].update(autoDeployTrigger="commit"),
    lambda cfg: cfg["services"][1].update(staticPublishPath="../private"),
    lambda cfg: cfg["services"][1].update(headers=[]),
    lambda cfg: next(v for v in cfg["services"][0]["envVars"]
                     if v["key"] == "INCIDENT_SUBMISSIONS_ENABLED").update(value="true"),
    lambda cfg: next(v for v in cfg["services"][0]["envVars"]
                     if v["key"] == "OIDC_ISSUER").update(value="https://unsafe.example", sync=True),
])
def test_unsafe_blueprint_changes_are_blocked(mutation):
    cfg = yaml.safe_load(SOURCE)
    mutation(cfg)
    with pytest.raises(ValueError):
        validate_blueprint(yaml.safe_dump(cfg))
