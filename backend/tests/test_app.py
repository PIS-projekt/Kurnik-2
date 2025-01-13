from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.psi_backend.app import app
from src.psi_backend.database.user import User
from src.psi_backend.routes.auth import get_current_user


@pytest.fixture
def test_user() -> User:
    """Fixture to create a test user."""
    return User(
        id=1, username="testuser", email="test@example.com", hashed_pwd="hashedpwd123"
    )


@pytest.fixture
def authorized_client(test_user: User) -> TestClient:
    """Fixture to create an authorized test client."""
    app.dependency_overrides[get_current_user] = lambda: test_user
    return TestClient(app)


def test_create_new_room(authorized_client: TestClient) -> None:
    """Test the /create-new-room endpoint."""
    with patch(
        "src.psi_backend.app.create_room", return_value="ABC123"
    ) as mock_create_room:
        response = authorized_client.get("/create-new-room")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Room created successfully",
        "room_code": "ABC123",
    }
    mock_create_room.assert_called_once()


def test_join_room_success(authorized_client: TestClient) -> None:
    """Test the /join-room endpoint for an existing room."""
    room_code = "ABC123"
    with patch(
        "src.psi_backend.app.check_room_exists", return_value=True
    ) as mock_check_room_exists:
        response = authorized_client.get(f"/join-room?room_code={room_code}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Room can be joined.",
        "room_code": room_code,
        "room_exists": True,
    }
    mock_check_room_exists.assert_called_once_with(room_code)


def test_join_room_not_found(authorized_client: TestClient) -> None:
    """Test the /join-room endpoint for a nonexistent room."""
    room_code = "NONEXISTENT"
    with patch(
        "src.psi_backend.app.check_room_exists", return_value=False
    ) as mock_check_room_exists:
        response = authorized_client.get(f"/join-room?room_code={room_code}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found."}
    mock_check_room_exists.assert_called_once_with(room_code)
