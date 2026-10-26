"""Isolated ephemeral SQLite database and explicit test-only credentials."""
import os
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///" + str(Path(tempfile.gettempdir()) / ("civicshield_test_" + str(os.getpid()) + ".db"))
os.environ["INCIDENT_SUBMISSIONS_ENABLED"] = "true"
os.environ["RESPONDER_API_KEY"] = "test-only-review-key"
os.environ.pop("CIVICSHIELD_MODEL_PATH", None)

from backend.app.db import Base, engine  # noqa: E402
from backend.app.main import app  # noqa: E402

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
