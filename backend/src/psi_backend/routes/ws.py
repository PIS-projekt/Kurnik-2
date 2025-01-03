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


ws_router = APIRouter()


@ws_router.websocket("/connect/{room_code}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_code: RoomCode,
    user_id: int,  # user_id=Depends(get_current_user_id) -> This should be used when introducing server-side user authentication. Right now, user_id is passed as a query parameter.
):
    await websocket.accept()

    try:
        assign_user_to_room(
            room_code,
            WebSocketUser(
                user_id=user_id,
                websocket_connection=websocket,
            ),
        )
    except RoomNotFoundError as e:
        websocket.close()

    try:
        while True:

            message = await websocket.receive_text()

            await broadcast_message(room_code, user_id, message)

    except WebSocketDisconnect:
        disconnect_user(room_code, user_id)
