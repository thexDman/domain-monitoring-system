import pytest
from app import app as backend_app


@pytest.fixture
def client():
    backend_app.config["TESTING"] = True

    with backend_app.test_client() as client:
        yield client
