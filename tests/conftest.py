import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

@pytest.fixture
def client():
    return TestClient(app)