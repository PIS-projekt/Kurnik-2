from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, select
from src.psi_backend.message import Message, close_database, create_database, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_database(engine)
    """Sets up the database schema before
    starting the app"""
    yield
    close_database(engine)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
