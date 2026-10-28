"""Verify that development convenience tools do not bake secrets into images."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_root_dockerignore_excludes_private_credentials_and_data():
    content = (ROOT / ".dockerignore").read_text("utf-8")
    for pattern in (".env", "backups/", "data/", "artifacts/", "frontend/"):
        assert pattern in content
    assert (ROOT / "backend" / "Dockerfile").is_file()

def test_frontend_dockerignore_blocks_node_modules_and_env():
    content = (ROOT / "frontend" / ".dockerignore").read_text("utf-8")
    for pattern in ("node_modules/", "dist/", ".env"):
        assert pattern in content

def test_windows_setup_never_prints_credential_or_clears_db_volume():
    start = (ROOT / "scripts/start-local.ps1").read_text("utf-8")
    stop = (ROOT / "scripts/stop-local.ps1").read_text("utf-8")
    assert "RandomNumberGenerator" in start
    assert "POSTGRES_PASSWORD" in start
    assert "docker compose up --build -d" in start
    assert "Write-Host $password" not in start
    assert "docker compose down" in stop
    assert "docker compose down -v\n" not in stop
