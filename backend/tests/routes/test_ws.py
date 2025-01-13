from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException, WebSocketDisconnect
from fastapi.testclient import TestClient

from src.psi_backend.database.user import User
from src.psi_backend.websocket_chat.room_assignment import create_room, rooms


@pytest.fixture
def test_client() -> TestClient:
    from src.psi_backend.app import app

    return TestClient(app)


@pytest.fixture
def test_user() -> User:
    """Fixture to create a test user."""
    return User(
        id=1, username="testuser", email="test@example.com", hashed_pwd="hashedpwd123"
    )


def test_connect_to_websocket_valid_user(
    test_client: TestClient, test_user: User, monkeypatch: pytest.MonkeyPatch
):

    new_room_code = create_room()

    def mock_get_current_user(_: str) -> User:
        return test_user

    monkeypatch.setattr(
        "src.psi_backend.routes.ws.get_current_user", mock_get_current_user
    )

    with test_client.websocket_connect(f"/ws/connect/{new_room_code}?token=123") as _:
        assert rooms[new_room_code][0].user_id == test_user.id


def test_connect_to_websocket_invalid_token(
    test_client: TestClient, test_user: User, monkeypatch: pytest.MonkeyPatch
):

    new_room_code = create_room()

    def mock_get_current_user_return_invalid(_: str):
        raise HTTPException(status_code=403, detail="Invalid token")

    monkeypatch.setattr(
        "src.psi_backend.routes.ws.get_current_user",
        mock_get_current_user_return_invalid,
    )

    with test_client.websocket_connect(
        f"/ws/connect/{new_room_code}?token=123"
    ) as websocket:
        with pytest.raises(WebSocketDisconnect) as exc:
            websocket.receive_text()

        assert exc.value.code == 1008
        assert exc.value.reason == "Invalid token"


def test_connect_to_websocket_missing_token(
    test_client: TestClient, test_user: User, monkeypatch: pytest.MonkeyPatch
):

    new_room_code = create_room()

    with test_client.websocket_connect(f"/ws/connect/{new_room_code}") as websocket:
        with pytest.raises(WebSocketDisconnect) as exc:
            websocket.receive_text()

        assert exc.value.code == 1008
        assert exc.value.reason == "Missing token"


def test_connect_to_non_existent_room(
    test_client: TestClient, test_user: User, monkeypatch: pytest.MonkeyPatch
):

    def mock_get_current_user(_: str) -> User:
        return test_user

    monkeypatch.setattr(
        "src.psi_backend.routes.ws.get_current_user", mock_get_current_user
    )
    with test_client.websocket_connect("/ws/connect/NOROOM?token=123") as websocket:

        with pytest.raises(WebSocketDisconnect) as exc:
            websocket.receive_text()

        # assert exc.value.code == 1003
        assert exc.value.reason == "Room not found"
