from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
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
    """A message in a chatroom. This class is used to interface
    with the DB."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)
    chatroom_id: int = Field(nullable=False)
    timestamp: datetime = Field(
        nullable=False,
        default_factory=lambda: datetime.now(),
    )
    contents: str = Field(nullable=False)


def main():

    with Session(engine) as session:

        msg = Message(
            user_id=1,
            chatroom_id=1,
            contents="Hello, world!",
        )
        session.add(msg)
        session.commit()

        statement = select(Message).where(Message.user_id == 1)
        messages = session.exec(statement).all()

        for message in messages:
            print(message.contents)
            print(message.timestamp)


if __name__ == "__main__":
    main()
