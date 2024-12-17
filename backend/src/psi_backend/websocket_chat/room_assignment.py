from dataclasses import dataclass
from fastapi import WebSocket
from collections import defaultdict
from src.psi_backend.message import Message, message_repository

UserID = int


@dataclass
class WebSocketUser:
    user_id: UserID
    websocket_connection: WebSocket


rooms: defaultdict[int, list[WebSocketUser]] = defaultdict(list)


def assign_user_to_room(room_id: int, user_websocket: WebSocketUser):
    """Assign the user to be inside a room

    Args:
        room_id (int): Room to put the user in.
        user_websocket (WebSocketUser): The user and his websocket connection.
    """
    rooms[room_id].append(user_websocket)


async def broadcast_message(room_id: int, user_id: int, message: str):
    """Broadcast a message to all users in the room.

    Args:
        room_id (int): Room to broadcast the message to.
        user_id (int): User that sent the message.
        message (str): Message to broadcast.
    """
    for websocket_user in rooms[room_id]:
        await websocket_user.websocket_connection.send_text(
            f"User[{user_id}] said: {message}."
        )
        message_repository.add_message(
            Message(user_id=user_id, chatroom_id=room_id, contents=message)
        )


def disconnect_user(room_id: int, user_id: int):
    """Disconnect the user from the room

    Args:
        room_id (int): Room to remove the user from.
        user_id (int): User to remove from the room.
    """
    for websocket_user in rooms[room_id]:
        if websocket_user.user_id == user_id:
            rooms[room_id].remove(websocket_user)
            break
    if not rooms[room_id]:
        del rooms[room_id]
