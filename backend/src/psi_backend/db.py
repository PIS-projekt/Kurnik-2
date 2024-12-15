from datetime import datetime
from sqlalchemy import Engine
from sqlmodel import Field, SQLModel, Session, create_engine, select
from attrs import define
from typing import Optional


DB_PROVIDER = "postgresql"
DB_DRIVER = "psycopg2"
# TODO: load using env vars depending on environment
DB_NAME = "pis"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "0.0.0.0"


engine = create_engine(
    f"{DB_PROVIDER}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)


class Message(SQLModel, table=True):
    """A message in a chatroom."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)
    chatroom_id: int = Field(nullable=False)
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

    def get_messages(self):
        """Gets all messages from the database."""
        with Session(self.engine) as session:
            messages = session.exec(select(Message)).all()
            return messages

    def delete_message(self, message_id: int):
        """Deletes a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(Message, message_id)
            if msg is None:
                raise MessageNotFoundError(f"Message with id {message_id} not found")

            session.delete(msg)
            session.commit()
