from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from src.psi_backend.database.db import (
    close_database,
    create_database,
    engine,
)

from src.psi_backend.database.user import User

from src.psi_backend.routes.auth import auth_router, get_current_user

from src.psi_backend.routes.ws import ws_router
from src.psi_backend.websocket_chat.room_assignment import (
    create_room,
    check_room_exists,
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
    allow_origins=["*"],  # Replace with the actual URL of your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/create-new-room")
async def create_room_endpoint(
    current_user: Annotated[User, Depends(get_current_user)]
):
    print(current_user.username)

    room_code = create_room()

    return {"message": "Room created successfully", "room_code": room_code}


@app.get("/join-room")
async def join_room(room_code: str, user: User = Depends(get_current_user)):
    """This endpoint has to be called before attempting to connect to the websocket endpoint."""
    if check_room_exists(room_code):
        return {
            "message": "Room can be joined.",
            "room_code": room_code,
            "room_exists": True,
        }
    else:
        raise HTTPException(status_code=404, detail="Room not found.")
