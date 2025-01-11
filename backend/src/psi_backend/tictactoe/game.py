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


@dataclass
class UpdateStateMessage:
    state: GameState

    @classmethod
    def create(cls, state: GameState):
        return cls(state=state)

    def json(self):
        return {
            "action": "update_state",
            "state": self.state.json(),
        }


@dataclass
class GameOverMessage:
    state: GameState
    winner: UserId

    @classmethod
    def create(cls, state: GameState, winner: UserId):
        return cls(state=state, winner=winner)

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

    @classmethod
    def create(cls, session_id: GameSessionId, user_id: UserId, state: GameState):
        return cls(session_id=session_id, user_id=user_id, state=state)

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
    message = UpdateStateMessage.create(session.state).json()
    await broadcast_message(session_id, message)


async def broadcast_winner_and_finish(session_id: GameSessionId, winner: UserId):
    session = game_sessions[session_id]
    message = GameOverMessage.create(session.state, winner).json()
    await broadcast_message(session_id, message)
    await end_session(session_id)


async def handle_place_mark(session_id: GameSessionId, user_id: UserId, message: dict):
    session = game_sessions[session_id]
    x, y = message["x"], message["y"]
    session.state.board[x][y] = "X" if user_id == session.user1.user_id else "O"
    session.state.turn = session.user1.user_id if session.state.turn == session.user2.user_id else session.user2.user_id

    winner = check_winner(session.state.board)
    winner_user_id = session.user1.user_id if winner == "X" else session.user2.user_id if winner == "O" else None
    if winner is not None:
        await broadcast_winner_and_finish(session_id, winner_user_id)
    else:
        await broadcast_game_state(session_id)


async def handle_join(websocket: WebSocket, session_id: GameSessionId, user_id: UserId):
    session = game_sessions[session_id]
    message = AcceptJoinMessage.create(session_id, user_id, session.state).json()
    await websocket.send_json(message)


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
                await handle_place_mark(session_id, user_id, message)
            elif message["action"] == "join":
                await handle_join(websocket, session_id, user_id)



    except Exception as e:
        print(e)


@tictactoe_router.get("/number-of-sessions")
async def number_of_sessions():
    return {"number_of_sessions": len(game_sessions)}
