from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

from attrs import define
from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, create_engine, select

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


class Message(SQLModel, table=True):
    """A message in a chatroom."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)
    chatroom_code: str = Field(nullable=False)
    timestamp: datetime = Field(
        nullable=False,
        default_factory=lambda: datetime.now(),
    )
    contents: str = Field(nullable=False)


class MessageNotFoundError(Exception):
    """Raised when a message is not found."""


@define
class MessageRepository:
    """An abstraction over the database for messages."""

    engine: Engine

    def add_message(self, message: Message):
        """Adds a message to the database."""
        with Session(self.engine) as session:
            session.add(message)
            session.commit()

    def add_messages(self, messages: list[Message]):
        """Adds multiple messages to the database."""
        with Session(self.engine) as session:
            session.add_all(messages)
            session.commit()

    def get_messages(self):
        """Gets all messages from the database."""
        with Session(self.engine) as session:
            messages = session.exec(select(Message)).all()
            return messages

    def get_message(self, message_id: int):
        """Gets a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(Message, message_id)
            if msg is None:
                raise MessageNotFoundError(f"Message with id {message_id} not found")
            return msg

    def delete_message(self, message_id: int):
        """Deletes a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(Message, message_id)
            if msg is None:
                raise MessageNotFoundError(f"Message with id {message_id} not found")

            session.delete(msg)
            session.commit()

    def delete_messages(self, messages: list[Message]):
        """Deletes all messages from the database."""
        with Session(self.engine) as session:
            for msg in messages:
                session.delete(msg)
            session.commit()


message_repository = MessageRepository(engine)
