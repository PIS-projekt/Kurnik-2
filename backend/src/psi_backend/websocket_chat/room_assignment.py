from dataclasses import dataclass
from fastapi import WebSocket
import string
import random

from src.psi_backend.database.message import Message, message_repository
from src.psi_backend.database.user import User

UserID = int
RoomCode = str


@dataclass
class WebSocketUser:
    user_id: UserID
    websocket_connection: WebSocket


rooms: dict[RoomCode, list[WebSocketUser]] = dict()


class RoomNotFoundError(Exception):
    """Raised when a room is not found."""


def assign_user_to_room(room_code: RoomCode, user_websocket: WebSocketUser):
    """Assign the user to be inside a room

    Args:
        room_code (RoomCode): Room to put the user in.
        user_websocket (WebSocketUser): The user and his websocket connection.
    """
    if room_code in rooms:
        rooms[room_code].append(user_websocket)
    else:
        raise RoomNotFoundError(f"Room with code {room_code} not found.")


async def broadcast_message(room_code: RoomCode, user: User, message: str):
    """Broadcast a message to all users in the room.

    Args:
        room_code (RoomCode): Room to broadcast the message to.
        user_id (str): User that sent the message.
        message (str): Message to broadcast.
    """
    message_repository.add_message(
        Message(user_id=user.id, chatroom_code=room_code, contents=message)
    )

    for websocket_user in rooms[room_code]:
        await websocket_user.websocket_connection.send_text(
            f"User[{user.username}] said: {message}"
        )


def disconnect_user(room_code: int, user_id: int):
    """Disconnect the user from the room

    Args:
        room_code (RoomCode): Room to remove the user from.
        user_id (int): User to remove from the room.
    """
    for websocket_user in rooms[room_code]:
        if websocket_user.user_id == user_id:
            rooms[room_code].remove(websocket_user)
            break
    if not rooms[room_code]:
        del rooms[room_code]


def create_room() -> RoomCode:
    """Create a new room and give it a unique 6-digit alphanumeric code."

    Returns:
        RoomCode: The unique 6-digit alphanumeric code of the room.
    """
    room_code = generate_room_code()

    rooms[room_code] = []
    return room_code


def generate_room_code() -> RoomCode:
    """Generate a 6-digit alphanumeric code for a room.

    Returns:
        str: A 6-digit alphanumeric code.
    """
    characters = string.ascii_letters + string.digits
    code = "".join(random.choices(characters, k=6))

    while code in rooms:
        code = "".join(random.choices(characters, k=6))

    return code


def check_room_exists(room_code: RoomCode) -> bool:
    """Check if a room exists.

    Args:
        room_code (RoomCode): Room to check.

    Returns:
        bool: True if the room exists, False otherwise.
    """
    return room_code in rooms
