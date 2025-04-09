import json
import pytest
from app import app

@pytest.fixture
def client():
    """Provides a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
