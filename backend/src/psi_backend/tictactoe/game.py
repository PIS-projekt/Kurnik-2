from dataclasses import dataclass

from fastapi import APIRouter, WebSocket

tictactoe_router = APIRouter()

GameSessionId = str
UserId = int

@dataclass
class GameUser:
    user_id: UserId
    websocket_connection: WebSocket


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
    user1: GameUser | None
    user2: GameUser | None
    state: GameState


game_sessions: dict[GameSessionId, GameSession] = dict()


def check_winner(board: list[list[str]]) -> str | None:
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None


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


async def broadcast_winner(session_id: GameSessionId, winner: UserId):
    session = game_sessions[session_id]

    message = {
        "action": "game_over",
        "state": session.state.json(),
        "winner": winner,
    }

    for user in [session.user1, session.user2]:
        if user is not None:
            await user.websocket_connection.send_json(message)

async def handle_place_mark(websocket: WebSocket, session_id: GameSessionId, user_id: UserId, message: dict):
    session = game_sessions[session_id]
    x, y = message["x"], message["y"]
    session.state.board[x][y] = "X" if user_id == session.user1.user_id else "O"
    session.state.turn = session.user1.user_id if session.state.turn == session.user2.user_id else session.user2.user_id

    winner = check_winner(session.state.board)
    winner_user_id = session.user1.user_id if winner == "X" else session.user2.user_id if winner == "O" else None
    if winner is not None:
        await broadcast_winner(session_id, winner_user_id)
    else:
        await broadcast_game_state(session_id)


async def handle_join(websocket: WebSocket, session_id: GameSessionId, user_id: UserId):
    session = game_sessions[session_id]
    await websocket.send_json(
        {"action": "accept_join", "session_id": session_id, "user_id": user_id, "state": session.state.json()})


@tictactoe_router.websocket("/game/{session_id}")
async def tictactoe_endpoint(
        websocket: WebSocket,
        session_id: GameSessionId,
        user_id: UserId,
):
    await websocket.accept()

    try:
        print(f"Connecting user {user_id} to session {session_id}")
        connect_user_to_session(
            session_id=session_id,
            user=GameUser(user_id, websocket)
        )
    except ValueError:
        websocket.close()

    try:
        while True:
            message = await websocket.receive_json()
            print("Received message", message)

            if message["action"] == "place_mark":
                await handle_place_mark(websocket, session_id, user_id, message)
            elif message["action"] == "join":
                await handle_join(websocket, session_id, user_id)



    except Exception as e:
        print(e)
