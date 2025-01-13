from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.psi_backend.database.db import close_database, create_database, engine
from src.psi_backend.database.user import User
from src.psi_backend.routes.auth import auth_router, get_current_user
from src.psi_backend.routes.ws import ws_router
from src.psi_backend.websocket_chat.room_assignment import (
    check_room_exists,
    create_room,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_database(engine)
    """Sets up the database schema before
    starting the app"""
    yield
    close_database(engine)


app = FastAPI(lifespan=lifespan)
app.include_router(ws_router, prefix="/ws")
app.include_router(auth_router, prefix="/auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class CreateRoomResponse(BaseModel):
    message: str
    room_code: str


@app.get("/create-new-room", response_model=CreateRoomResponse)
def create_room_endpoint(
    _: Annotated[User, Depends(get_current_user)]
) -> CreateRoomResponse:

    room_code = create_room()

    return CreateRoomResponse(message="Room created successfully", room_code=room_code)


class JoinRoomResponse(BaseModel):
    message: str
    room_code: str
    room_exists: bool


@app.get("/join-room")
def join_room(room_code: str, _: User = Depends(get_current_user)) -> JoinRoomResponse:
    """This endpoint has to be called before attempting to connect to the
    websocket endpoint."""
    if check_room_exists(room_code):
        return JoinRoomResponse(
            message="Room can be joined.", room_code=room_code, room_exists=True
        )
    else:
        raise HTTPException(status_code=404, detail="Room not found.")
