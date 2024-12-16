from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from src.psi_backend.message import close_database, create_database, engine
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
