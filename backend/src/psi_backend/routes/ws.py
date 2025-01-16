from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.psi_backend.routes.auth import validate_websocket
from src.psi_backend.websocket_chat.room_assignment import (
    RoomNotFoundError,
    WebSocketUser,
    assign_user_to_room,
    broadcast_message,
    disconnect_user,
)

ws_router = APIRouter()


@ws_router.websocket("/connect/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str) -> None:
    await websocket.accept()

    token = websocket.query_params.get("token") or ""
    user = await validate_websocket(token, websocket)

    if user.id is None:
        return

    try:
        assign_user_to_room(
            room_code,
            WebSocketUser(
                user_id=user.id,
                websocket_connection=websocket,
            ),
        )
    except RoomNotFoundError:
        await websocket.close(code=1003, reason="Room not found")
        return

    try:
        while True:
            message = await websocket.receive_text()
            await broadcast_message(room_code, user, message)

    except WebSocketDisconnect:
        disconnect_user(room_code, user.id)
