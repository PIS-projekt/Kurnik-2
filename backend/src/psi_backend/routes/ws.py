from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from src.psi_backend.websocket_chat.room_assignment import (
    RoomNotFoundError,
    assign_user_to_room,
    broadcast_message,
    disconnect_user,
    WebSocketUser,
    RoomCode,
)

from src.psi_backend.routes.auth import get_current_user, OAuth2PasswordBearer

from src.psi_backend.database.user import User


ws_router = APIRouter()


from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


@ws_router.websocket("/connect/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await websocket.accept()

    # Extract the token from the query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Missing token")
        print("Missing token")
        return

    # Validate the token and get the current user
    try:
        user = await get_current_user(token)
        print(user)
    except HTTPException as e:
        await websocket.close(code=1008, reason="Invalid token")
        return

    try:
        assign_user_to_room(
            room_code,
            WebSocketUser(
                user_id=user.id,
                websocket_connection=websocket,
            ),
        )
    except RoomNotFoundError as e:
        await websocket.close(code=1003, reason="Room not found")
        return

    try:
        while True:
            message = await websocket.receive_text()
            await broadcast_message(room_code, user, message)

    except WebSocketDisconnect:
        disconnect_user(room_code, user.id)
