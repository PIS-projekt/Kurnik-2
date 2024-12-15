from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select
from src.psi_backend.db import Message, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    """Sets up the database schema before
    starting the app"""
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
