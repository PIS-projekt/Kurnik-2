from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.psi_backend.message import (
    close_database,
    create_database,
    engine,
    message_repository,
)
from src.psi_backend.routes.ws import ws_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_database(engine)
    """Sets up the database schema before
    starting the app"""
    yield
    close_database(engine)


app = FastAPI(lifespan=lifespan)
app.include_router(ws_router, prefix="/ws")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/messages")
async def read_messages():
    return message_repository.get_messages()
