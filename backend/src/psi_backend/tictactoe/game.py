from dataclasses import dataclass

from fastapi import APIRouter, WebSocket

tictactoe_router = APIRouter()

GameSessionId = str


@dataclass
class GameUser:
    user_id: int
    websocket_connection: WebSocket


@dataclass
class GameState:
    board: list[list[str]]
    turn: int

    def json(self):
        return {
            "board": self.board,
            "turn": self.turn,
        }


@dataclass
class GameSession:
    id: GameSessionId
    user1: GameUser | None
    user2: GameUser | None
    state: GameState


game_sessions: dict[GameSessionId, GameSession] = dict()


def connect_user_to_session(session_id: GameSessionId, user: GameUser):
    if session_id in game_sessions:
        if game_sessions[session_id].user1 is None:
            game_sessions[session_id].user1 = user
        elif game_sessions[session_id].user2 is None:
            game_sessions[session_id].user2 = user
        else:
            raise ValueError("Session is full")
    else:
        game_sessions[session_id] = GameSession(
            id=session_id,
            user1=user,
            user2=None,
            state=GameState(board=[["", "", ""], ["", "", ""], ["", "", ""]], turn=user.user_id),
        )


async def broadcast_game_state(session_id: GameSessionId):
    session = game_sessions[session_id]

    message = {
        "action": "update_state",
        "state": session.state.json(),
    }

    for user in [session.user1, session.user2]:
        if user is not None:
            await user.websocket_connection.send_json(message)


async def handle_place_mark(websocket: WebSocket, room_code: str, user_id: int, message: dict):
    session = game_sessions[room_code]
    x, y = message["x"], message["y"]
    session.state.board[x][y] = "X" if user_id == session.user1.user_id else "O"
    session.state.turn = session.user1.user_id if session.state.turn == session.user2.user_id else session.user2.user_id

    await broadcast_game_state(room_code)


async def handle_join(websocket: WebSocket, room_code: str, user_id: int):
    session = game_sessions[room_code]
    await websocket.send_json(
        {"action": "accept_join", "room_code": room_code, "user_id": user_id, "state": session.state.json()})


@tictactoe_router.websocket("/game/{room_code}")
async def tictactoe_endpoint(
        websocket: WebSocket,
        room_code: str,
        user_id: int,
):
    await websocket.accept()

    try:
        print(f"Connecting user {user_id} to session {room_code}")
        connect_user_to_session(
            session_id=room_code,
            user=GameUser(user_id, websocket)
        )
    except ValueError:
        websocket.close()

    try:
        while True:
            message = await websocket.receive_json()
            print("Received message", message)

            if message["action"] == "place_mark":
                await handle_place_mark(websocket, room_code, user_id, message)
            elif message["action"] == "join":
                await handle_join(websocket, room_code, user_id)



    except Exception as e:
        print(e)
