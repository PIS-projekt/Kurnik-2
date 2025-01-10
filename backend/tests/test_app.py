import pytest
from fastapi.testclient import TestClient
from httpx import Response

from src.psi_backend.app import app

client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def mock_room_code_randomness(monkeypatch):
    """Mock the randomness of the room code generator.
    Generates room codes in the format "ABC123", "ABC124", "ABC125", ..."""

    prefix = "ABC"
    current_suffix = 122

    def code_gen():
        nonlocal current_suffix
        current_suffix += 1
        return prefix + str(current_suffix)

    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.generate_room_code",
        code_gen,
    )


# Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


# Test join room failure
def test_join_room_failure(monkeypatch):
    def mock_check_room_exists(_):
        return False

    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.check_room_exists",
        mock_check_room_exists,
    )

    response = client.get("/join-room", params={"room_code": "ABC123", "user_id": 1234})

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found."}


def request_room_creation(private: bool) -> Response:
    return client.get(
        "/create-new-room", params={"private": str(private).lower(), "user_id": 1234}
    )


def test_mock_room_code_randomness():
    from src.psi_backend.websocket_chat.room_assignment import generate_room_code

    assert generate_room_code() == "ABC123"
    assert generate_room_code() == "ABC124"
    assert generate_room_code() == "ABC125"


def test_create_rooms():
    response = request_room_creation(private=False)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Room created successfully",
        "room_code": "ABC123",
        "private": "False",
    }

    response = request_room_creation(private=True)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Room created successfully",
        "room_code": "ABC124",
        "private": "True",
    }
