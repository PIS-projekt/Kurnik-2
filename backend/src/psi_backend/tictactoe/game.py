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
    counter: int
    turn: int


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
            state=GameState(counter=0, turn=1),
        )


async def broadcast_game_state(session_id: GameSessionId):
    session = game_sessions[session_id]

    message = {
        "action": "update_state",
        "state": {
            "counter": session.state.counter,
            "turn": session.state.turn,
        },
    }

    for user in [session.user1, session.user2]:
        if user is not None:
            await user.websocket_connection.send_json(message)


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
            print("Receiver message", message)
            session = game_sessions[room_code]

            session.state.counter += 1
            session.state.turn = 1 if session.state.turn == 2 else 2

            await broadcast_game_state(room_code)

    except Exception as e:
        print(e)
