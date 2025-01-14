from dataclasses import dataclass
from typing import Optional, cast

from fastapi import APIRouter, WebSocket

from src.psi_backend.websocket_chat.room_assignment import WebSocketUser
from src.psi_backend.routes.auth import validate_websocket

tictactoe_router = APIRouter()

GameSessionId = str
UserId = int


@dataclass
class GameState:
    board: list[list[str]]
    turn: UserId

    def json(self):
        return {
            "board": self.board,
            "turn": self.turn,
        }


@dataclass
class GameSession:
    id: GameSessionId
    user1: Optional[WebSocketUser]
    user2: Optional[WebSocketUser]
    state: GameState


@dataclass
class UpdateStateMessage:
    state: GameState

    def json(self):
        return {
            "action": "update_state",
            "state": self.state.json(),
        }


@dataclass
class GameOverMessage:
    state: GameState
    winner: Optional[UserId]

    def json(self):
        return {
            "action": "game_over",
            "state": self.state.json(),
            "winner": self.winner,
        }


@dataclass
class AcceptJoinMessage:
    session_id: GameSessionId
    user_id: UserId
    state: GameState

    def json(self):
        return {
            "action": "accept_join",
            "session_id": self.session_id,
            "user_id": self.user_id,
            "state": self.state.json(),
        }


game_sessions: dict[GameSessionId, GameSession] = dict()


def empty_board():
    return [["", "", ""], ["", "", ""], ["", "", ""]]


def check_winner(board: list[list[str]]) -> tuple[bool, Optional[str]]:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return True, board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return True, board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != "":
        return True, board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True, board[0][2]

    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return True, None  # draw

    return False, None


def connect_user_to_session(session_id: GameSessionId, user: WebSocketUser):
    if session_id in game_sessions:
        if game_sessions[session_id].user1 is None:
            game_sessions[session_id].user1 = user
        elif game_sessions[session_id].user2 is None:
            game_sessions[session_id].user2 = user
        else:
            raise ValueError("Session is full")
    else:
        print(f"Creating new session {session_id}")
        game_sessions[session_id] = GameSession(
            id=session_id,
            user1=user,
            user2=None,
            state=GameState(board=empty_board(), turn=user.user_id),
        )


async def end_session(session_id: GameSessionId):
    session = game_sessions[session_id]
    await session.user1.websocket_connection.close()
    await session.user2.websocket_connection.close()
    game_sessions.pop(session_id)


async def broadcast_message(session_id: GameSessionId, message_json: dict):
    session = game_sessions[session_id]

    for user in [session.user1, session.user2]:
        if user is not None:
            await user.websocket_connection.send_json(message_json)


async def broadcast_game_state(session_id: GameSessionId):
    session = game_sessions[session_id]
    message = UpdateStateMessage(session.state).json()
    await broadcast_message(session_id, message)


async def broadcast_winner_and_finish(
    session_id: GameSessionId, winner: Optional[UserId]
):
    session = game_sessions[session_id]
    message = GameOverMessage(session.state, winner).json()
    await broadcast_message(session_id, message)
    await end_session(session_id)


async def handle_place_mark(session_id: GameSessionId, user_id: UserId, message: dict):
    session = game_sessions[session_id]
    user1, user2 = cast(WebSocketUser, session.user1), cast(
        WebSocketUser, session.user2
    )
    x, y = message["x"], message["y"]
    session.state.board[x][y] = "X" if user_id == user1.user_id else "O"
    session.state.turn = (
        user1.user_id if session.state.turn == user2.user_id else user2.user_id
    )

    game_over, winner = check_winner(session.state.board)
    if game_over:
        winner_user_id = (
            user1.user_id if winner == "X" else user2.user_id if winner == "O" else None
        )
        await broadcast_winner_and_finish(session_id, cast(int, winner_user_id))
    else:
        await broadcast_game_state(session_id)


async def handle_join(websocket: WebSocket, session_id: GameSessionId, user_id: UserId):
    session = game_sessions[session_id]
    message = AcceptJoinMessage(session_id, user_id, session.state).json()
    await websocket.send_json(message)


@tictactoe_router.websocket("/game/{session_id}")
async def tictactoe_endpoint(
    websocket: WebSocket,
    session_id: GameSessionId,
    token: str,
):
    await websocket.accept()

    token = websocket.query_params.get("token") or ""
    user = await validate_websocket(token, websocket)

    if user.id is None:
        return

    try:
        print(f"Connecting user {user.id} to session {session_id}")
        connect_user_to_session(
            session_id=session_id, user=WebSocketUser(user.id, websocket)
        )
    except ValueError:
        await websocket.close()

    try:
        while True:
            message = await websocket.receive_json()
            print("Received message", message)
            print("Turn of ", game_sessions[session_id].state.turn)
            if message["action"] == "place_mark":
                await handle_place_mark(session_id, user.id, message)
            elif message["action"] == "join":
                await handle_join(websocket, session_id, user.id)
    except Exception as e:
        print(e)


@tictactoe_router.get("/number-of-sessions")
async def number_of_sessions():
    return {"number_of_sessions": len(game_sessions)}
