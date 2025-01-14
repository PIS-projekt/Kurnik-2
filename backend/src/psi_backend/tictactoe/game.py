from dataclasses import dataclass
from loguru import logger
from typing import Optional, cast

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel

from src.psi_backend.websocket_chat.room_assignment import WebSocketUser
from src.psi_backend.routes.auth import validate_websocket

tictactoe_router = APIRouter()

GameSessionId = str
UserId = int


class SessionFullError(Exception):
    """Thrown when a user tries to join a full session."""


from typing import List, Optional
from pydantic import BaseModel


class GameState(BaseModel):
    board: List[List[str]]
    turn: UserId


@dataclass
class GameSession:
    id: GameSessionId
    user1: Optional[WebSocketUser]
    user2: Optional[WebSocketUser]
    state: GameState

    def players_present(self):
        """Check if both players are present and the game can start."""
        return self.user1 is not None and self.user2 is not None

    def get_player_by_id(self, user_id: UserId) -> Optional[WebSocketUser]:
        if self.user1 is not None and self.user1.user_id == user_id:
            return self.user1
        elif self.user2 is not None and self.user2.user_id == user_id:
            return self.user2
        return None


class UpdateStateMessage(BaseModel):
    action: str = "update_state"
    state: GameState


class GameOverMessage(BaseModel):
    action: str = "game_over"
    state: GameState
    winner: Optional[UserId]


class AcceptJoinMessage(BaseModel):
    action: str = "accept_join"
    session_id: GameSessionId
    user_id: UserId
    state: GameState


class ErrorMessage(BaseModel):
    action: str = "error"
    message: str


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


async def connect_user_to_session(session_id: GameSessionId, user: WebSocketUser):
    if session_id in game_sessions:
        if game_sessions[session_id].user1 is None:
            game_sessions[session_id].user1 = user
        elif game_sessions[session_id].user2 is None:
            game_sessions[session_id].user2 = user
        else:
            logger.info(f"Session {session_id} is full")
            await user.websocket_connection.send_json(
                ErrorMessage(message="Game is full").model_dump()
            )
            raise SessionFullError()
    else:
        logger.info(f"Creating new session {session_id}")
        game_sessions[session_id] = GameSession(
            id=session_id,
            user1=user,
            user2=None,
            state=GameState(board=empty_board(), turn=user.user_id),
        )


async def end_session(session_id: GameSessionId):
    session = game_sessions[session_id]
    u1, u2 = cast(WebSocketUser, session.user1), cast(WebSocketUser, session.user2)
    await u1.websocket_connection.close()
    await u2.websocket_connection.close()
    game_sessions.pop(session_id)


async def broadcast_message(session_id: GameSessionId, message_json: dict):
    session = game_sessions[session_id]

    for user in [session.user1, session.user2]:
        if user is not None:
            await user.websocket_connection.send_json(message_json)


async def broadcast_game_state(session_id: GameSessionId):
    session = game_sessions[session_id]
    message = UpdateStateMessage(state=session.state).model_dump()
    await broadcast_message(session_id, message)


async def broadcast_winner_and_finish(
    session_id: GameSessionId, winner: Optional[UserId]
):
    session = game_sessions[session_id]
    message = GameOverMessage(state=session.state, winner=winner).model_dump()
    await broadcast_message(session_id, message)
    await end_session(session_id)


async def handle_premature_move(session_id: GameSessionId, user_id: UserId):
    """Handle a move from a player who is not supposed to move since the
    game has not been started yet."""
    player = cast(WebSocketUser, game_sessions[session_id].get_player_by_id(user_id))
    await player.websocket_connection.send_json(
        ErrorMessage(
            message="Unable to make a move before opponent joins."
        ).model_dump()
    )


async def handle_place_mark(session_id: GameSessionId, user_id: UserId, message: dict):
    session = game_sessions[session_id]

    if not session.players_present():
        await handle_premature_move(session_id, user_id)
        return

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
    message = AcceptJoinMessage(
        session_id=session_id, user_id=user_id, state=session.state
    ).model_dump()
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
        await connect_user_to_session(
            session_id=session_id, user=WebSocketUser(user.id, websocket)
        )
    except (ValueError, SessionFullError):
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
