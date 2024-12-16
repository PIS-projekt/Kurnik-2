from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from src.psi_backend.websocket_chat.room_assignment import (
    assign_user_to_room,
    broadcast_message,
    disconnect_user,
    WebSocketUser,
)


ws_router = APIRouter()


@ws_router.get("/websocket_client_simulation")
async def websocket_client_simulation():
    """
    This endpoint serves an HTML page that simulates a client connecting to the chat. This part will be done on the frontend in production.
    """

    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>ChatRoom</title>
        </head>
        <body>
            <h1>WebSocket ChatRoom</h1>
            <form action="" onsubmit="joinRoom(event)">
                <label for="room">Room Name:</label>
                <input type="text" id="room" />
                <label for="user_id">User ID:</label>
                <input type="text" id="user_id" />
                <button>Join Room</button>
            </form>
            <div id="chat"></div>
            <input type="text" id="message" placeholder="Type your message here..." />
            <button onclick="sendMessage()">Send Message</button>
            <script>
                let websocket;
                function joinRoom(event) {
                    event.preventDefault();
                    const room = document.getElementById('room').value;
                    const user_id = document.getElementById('user_id').value;
                    websocket = new WebSocket(`ws://localhost:8000/ws/${room}?user_id=${user_id}`);

                    websocket.onopen = function() {
                        const chat = document.getElementById('chat');
                        const confirmation = document.createElement('div');
                        confirmation.textContent = `Successfully joined room: ${room}`;
                        chat.appendChild(confirmation);
                    };

                    websocket.onmessage = function(event) {
                        const chat = document.getElementById('chat');
                        const message = document.createElement('div');
                        message.textContent = event.data;
                        chat.appendChild(message);
                    };

                    websocket.onclose = function() {
                        const chat = document.getElementById('chat');
                        const message = document.createElement('div');
                        message.textContent = 'Connection closed';
                        chat.appendChild(message);
                    };
                }

                function sendMessage() {
                    const messageInput = document.getElementById('message');
                    const message = messageInput.value;
                    if (websocket && websocket.readyState === WebSocket.OPEN) {
                        websocket.send(message);
                        messageInput.value = '';
                    }
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@ws_router.websocket("/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    user_id: int,  # user_id=Depends(get_current_user_id) -> This should be used when introducing server-side user authentication. Right now, user_id is passed as a query parameter.
):
    await websocket.accept()

    assign_user_to_room(
        room_id,
        WebSocketUser(
            user_id=user_id,
            websocket_connection=websocket,
        ),
    )

    try:
        while True:

            message = await websocket.receive_text()

            await broadcast_message(room_id, user_id, message)

    except WebSocketDisconnect:
        disconnect_user(room_id, user_id)
