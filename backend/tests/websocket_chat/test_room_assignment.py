import pytest
from fastapi import WebSocket
from unittest.mock import AsyncMock
from src.psi_backend.websocket_chat.room_assignment import (
    assign_user_to_room,
    disconnect_user,
    create_room,
    generate_room_code,
    check_room_exists,
    RoomNotFoundError,
    WebSocketUser,
    rooms,
)


@pytest.fixture
def websocket_user() -> WebSocketUser:
    """Fixture to create a WebSocketUser."""
    mock_websocket = AsyncMock(spec=WebSocket)
    return WebSocketUser(user_id=1, websocket_connection=mock_websocket)


def test_create_room() -> None:
    """Test room creation and uniqueness of the room code."""
    room_code = create_room()
    assert len(room_code) == 6
    assert room_code in rooms


def test_generate_room_code() -> None:
    """Test that the generated room code is a 6-character alphanumeric string."""
    room_code = generate_room_code()
    assert len(room_code) == 6
    assert room_code.isalnum()


def test_assign_user_to_room_existing_room(websocket_user: WebSocketUser) -> None:
    """Test assigning a user to an existing room."""
    room_code = create_room()
    assign_user_to_room(room_code, websocket_user)
    assert len(rooms[room_code]) == 1
    assert rooms[room_code][0] == websocket_user


def test_assign_user_to_room_nonexistent_room(websocket_user: WebSocketUser) -> None:
    """Test assigning a user to a nonexistent room raises an error."""
    with pytest.raises(
        RoomNotFoundError, match="Room with code invalid_code not found."
    ):
        assign_user_to_room("invalid_code", websocket_user)


def test_disconnect_user(websocket_user: WebSocketUser) -> None:
    """Test disconnecting a user from a room."""
    room_code = create_room()
    rooms[room_code].append(websocket_user)

    disconnect_user(room_code, websocket_user.user_id)
    assert check_room_exists(room_code) is False


def test_check_room_exists() -> None:
    """Test checking if a room exists."""
    room_code = create_room()
    assert check_room_exists(room_code) is True
    assert check_room_exists("nonexistent") is False
