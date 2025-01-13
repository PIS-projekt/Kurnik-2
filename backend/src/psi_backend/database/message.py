from __future__ import annotations
from datetime import datetime
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, select
from sqlmodel import Field  # type: ignore
from attrs import define
from typing import Optional, Sequence

from src.psi_backend.database.db import engine


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

    def add_message(self, message: Message) -> None:
        """Adds a message to the database."""
        with Session(self.engine) as session:
            session.add(message)
            session.commit()

    def add_messages(self, messages: list[Message]) -> None:
        """Adds multiple messages to the database."""
        with Session(self.engine) as session:
            session.add_all(messages)
            session.commit()

    def get_messages(self) -> Sequence[Message]:
        """Gets all messages from the database."""
        with Session(self.engine) as session:
            messages = session.exec(select(Message)).all()
            return messages

    def get_message(self, message_id: int) -> Message:
        """Gets a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(Message, message_id)
            if msg is None:
                raise MessageNotFoundError(f"Message with id {message_id} not found")
            return msg

    def delete_message(self, message_id: int) -> None:
        """Deletes a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(Message, message_id)
            if msg is None:
                raise MessageNotFoundError(f"Message with id {message_id} not found")

            session.delete(msg)
            session.commit()

    def delete_messages(self, messages: Sequence[Message]) -> None:
        """Deletes all messages from the database."""
        with Session(self.engine) as session:
            for msg in messages:
                session.delete(msg)
            session.commit()


message_repository = MessageRepository(engine)
