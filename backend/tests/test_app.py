from fastapi.testclient import TestClient

from src.psi_backend.app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_fails():
    assert False
