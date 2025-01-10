from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from src.psi_backend.app import app
from src.psi_backend.websocket_chat.room_assignment import RoomNotFoundError

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_assign_user_to_room(monkeypatch):
    async def mock(room_code, _):
        if room_code != "VALID123":
            raise RoomNotFoundError("Room not found")

    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.assign_user_to_room", mock
    )
    return mock


@pytest.fixture(autouse=True)
def mock_broadcast_message(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.broadcast_message", mock
    )
    return mock


@pytest.fixture(autouse=True)
def mock_disconnect_user(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.disconnect_user", mock
    )
    return mock


@pytest.fixture(autouse=True)
def mock_rooms(monkeypatch):
    monkeypatch.setattr(
        "src.psi_backend.websocket_chat.room_assignment.rooms",
        {"VALID123": []},
    )
