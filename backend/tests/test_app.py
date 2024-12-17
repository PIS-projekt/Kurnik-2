import pytest
from fastapi.testclient import TestClient
from src.psi_backend.app import app

client = TestClient(app)


# Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


# Test room creation endpoint
def test_create_new_room(monkeypatch):
    def mock_create_room(user_id):
        return "ABC123"

    monkeypatch.setattr("src.psi_backend.app.create_room", mock_create_room)

    response = client.get("/create-new-room", params={"user_id": 1234})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Room created successfully",
        "room_code": "ABC123",
    }


# Test join room success
def test_join_room_success(monkeypatch):
    def mock_check_room_exists(room_code):
        return True

    monkeypatch.setattr("src.psi_backend.app.check_room_exists", mock_check_room_exists)

    response = client.get("/join-room", params={"room_code": "ABC123", "user_id": 1234})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Room can be joined.",
        "room_code": "ABC123",
        "room_exists": True,
    }


# Test join room failure
def test_join_room_failure(monkeypatch):
    def mock_check_room_exists(room_code):
        return False

    monkeypatch.setattr("src.psi_backend.app.check_room_exists", mock_check_room_exists)

    response = client.get("/join-room", params={"room_code": "ABC123", "user_id": 1234})

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found."}
