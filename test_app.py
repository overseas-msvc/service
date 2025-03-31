
import json
import pytest
from app import app

@pytest.fixture
def client():
    """Provides a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_service(client):
    response = client.get("/service", json={'id': 1})
    assert response.status_code == 200
    assert json.loads(response.get_data()) == "reply from endpoint get_service, data = {'id': 1}"

def test_create_service(client):
    response = client.post("/service", json={'name': 'sample_string'})
    assert response.status_code == 200
    assert json.loads(response.get_data()) == "reply from endpoint create_service, data = {'name': 'sample_string'}"
