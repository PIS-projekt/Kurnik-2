from __future__ import annotations
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine
import os

DB_PROVIDER = "postgresql"
DB_DRIVER = "psycopg2"
# TODO: load using env vars depending on environment
DB_NAME = "pis"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = os.getenv("DB_HOST") or "0.0.0.0"


engine = create_engine(
    f"{DB_PROVIDER}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)


def create_database(engine: Engine):
    """Creates the database schema using a given engine."""
    SQLModel.metadata.create_all(engine)


def close_database(engine: Engine):
    """Closes the database connection."""
    engine.dispose()
