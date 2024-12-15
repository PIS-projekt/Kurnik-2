from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, create_engine
from sqlalchemy.orm import Session, declarative_base

DB_PROVIDER = "postgresql"
DB_DRIVER = "psycopg2"
# TODO: load using env vars depending on environment
DB_NAME = "pis"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "0.0.0.0"


Base = declarative_base()
engine = create_engine(
    f"{DB_PROVIDER}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    echo=True,
)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    chatroom_id = Column(Integer, nullable=False)
    timestamp = Column(BigInteger, nullable=False)  # Unix timestamp in milliseconds
    contents = Column(String, nullable=False)


def setup_schema():
    Base.metadata.create_all(engine)


def main():
    setup_schema()
    session = Session(engine)
    msg = Message(
        user_id=1, chatroom_id=1, timestamp=1638422400000, contents="Hello, world!"
    )
    session.add(msg)
    session.commit()
    # select all messages
    messages = session.query(Message).all()
    for message in messages:
        print(message.contents)


if __name__ == "__main__":
    main()
