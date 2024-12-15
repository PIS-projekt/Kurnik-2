from contextlib import asynccontextmanager

from fastapi import FastAPI

from psi_backend.db import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Sets up the database schema before
    starting the app"""
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
