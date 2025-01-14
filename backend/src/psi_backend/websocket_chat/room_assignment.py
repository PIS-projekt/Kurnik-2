from __future__ import annotations

import random
import string
from dataclasses import dataclass, field
import random
import string
from dataclasses import dataclass

from fastapi import WebSocket

from src.psi_backend.database.message import Message, message_repository
from src.psi_backend.database.user import User

UserID = int
RoomCode = str
rooms: dict[RoomCode, Chatroom] = dict()


def delete_room(room_code: RoomCode):
    """Remove a room from the rooms dictionary."""
    del rooms[room_code]


def delete_room_if_empty(room_code: RoomCode):
    """Remove a room from the rooms dictionary if it is empty."""
    if rooms[room_code].is_empty():
        delete_room(room_code)


def check_room_exists(room_code: RoomCode) -> bool:
    """Check if a room exists.

    Args:
        room_code (RoomCode): Room to check.

    Returns:
        bool: True if the room exists, False otherwise.
    """
    return room_code in rooms


@dataclass
class WebSocketUser:
    user_id: UserID
    websocket_connection: WebSocket


@dataclass
class Chatroom:
    """A room consisting of a list of users. Rooms can be public or private"""

    id: RoomCode
    private: bool = field(default=False)
    users: list[WebSocketUser] = field(default_factory=list)

    def add_user(self, user: WebSocketUser):
        """Add a user to the room."""
        self.users.append(user)

    def remove_user(self, user_id: UserID):
        """Remove a user from the room."""
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                break
        # TODO: might want to throw an error here?

    def is_empty(self) -> bool:
        """Check if the room is empty."""
        return not self.users

    async def message_all(self, message: str):
        """Send a message to all users in the room."""
        for user in self.users:
            await user.websocket_connection.send_text(message)


class RoomNotFoundError(Exception):
    """Raised when a room is not found."""


def assign_user_to_room(room_code: RoomCode, user_websocket: WebSocketUser):
    """Assign the user to be inside a room

    Args:
        room_code (RoomCode): Room to put the user in.
        user_websocket (WebSocketUser): The user and his websocket connection.
    """
    if room_code in rooms:
        rooms[room_code].add_user(user_websocket)
    else:
        raise RoomNotFoundError(f"Room with code {room_code} not found.")


async def broadcast_message(room_code: RoomCode, user: User, message: str) -> None:
    """Broadcast a message to all users in the room.

    Args:
        room_code (RoomCode): Room to broadcast the message to.
        user_id (str): User that sent the message.
        message (str): Message to broadcast.
    """
    if user.id is None:
        raise ValueError("User ID cannot be None")

    message_repository.add_message(
        Message(user_id=user.id, chatroom_code=room_code, contents=message)
    )

    if room_code not in rooms:
        raise RoomNotFoundError(f"Room with code {room_code} not found.")

    await rooms[room_code].message_all(f"{user.username} said: {message}")


def disconnect_user(room_code: RoomCode, user_id: int) -> None:
    """Disconnect the user from the room

    Args:
        room_code (RoomCode): Room to remove the user from.
        user_id (int): User to remove from the room.
    """
    room = rooms[room_code]
    room.remove_user(user_id)
    delete_room_if_empty(room_code)


def create_room(private: bool) -> RoomCode:
    """Create a new room and give it a unique 6-digit alphanumeric code."

    Returns:
        RoomCode: The unique 6-digit alphanumeric code of the room.
    """
    room_code = generate_room_code()

    rooms[room_code] = Chatroom(room_code, private)
    return room_code


def generate_room_code() -> RoomCode:
    """Generate a 6-digit alphanumeric code for a room.

    Returns:
        str: A 6-digit alphanumeric code.
    """

    def get_new_code() -> str:
        """Get a new random room code"""
        return "".join(random.choices(string.ascii_letters + string.digits, k=6))

    code = get_new_code()
    while code in rooms:
        code = get_new_code()

    return code
