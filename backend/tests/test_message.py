from sqlmodel import create_engine
from copy import deepcopy
from src.psi_backend.message import (
    Message,
    MessageNotFoundError,
    MessageRepository,
    create_database,
)
from pytest import fixture, raises


def temporary_db():
    """An in-memory sqlite database."""
    engine = create_engine("sqlite://")
    create_database(engine)
    return engine


def temporary_repo(contents: list[Message] = []):
    """MessageRepository over an in memory sqlite DB"""
    engine = temporary_db()
    repo = MessageRepository(engine)
    repo.add_messages(contents)
    return repo


def weak_message_eq(msg1, msg2):
    """Weak equality for messages, used only for
    performing insertion tests, so added here not to clutter the message class."""
    return (
        msg1.user_id == msg2.user_id
        and msg1.chatroom_id == msg2.chatroom_id
        and msg1.contents == msg2.contents
        and msg1.timestamp == msg2.timestamp
    )


@fixture
def prepopulated_repo():
    """A pre-populated message repository for testing purposes."""
    messages = [
        Message(user_id=1, chatroom_id=1, contents="Hello, world!"),
        Message(user_id=2, chatroom_id=1, contents="Goodbye, world!"),
        Message(user_id=1, chatroom_id=2, contents="Hello, universe!"),
        Message(user_id=1, chatroom_id=2, contents="Hello, szmozo de la dziobo!"),
    ]
    yield temporary_repo(messages)


def test_add_message():
    """Adds a single message and retrieves it. Since the message object gets
    cleared upon repo write, it has to be copied before insertion to compare.
    Since its deepcopy implementation does not copy the id, weak_message_eq has
    to be used."""
    repo = temporary_repo()
    message = Message(user_id=1, chatroom_id=1, contents="Hello, world!")
    copy = deepcopy(message)
    repo.add_message(message)
    assert weak_message_eq(repo.get_messages()[0], copy)


def test_add_messages():
    """Adds multiple messages and retrieves them. Check test_add_message
    for explanation of the way it's tested"""
    repo = temporary_repo()
    messages = [
        Message(user_id=1, chatroom_id=1, contents="Hello, world!"),
        Message(user_id=2, chatroom_id=1, contents="Goodbye, world!"),
    ]
    copies = deepcopy(messages)
    repo.add_messages(messages)  # Messages get cleared upon save, have to copy them
    results = repo.get_messages()

    for m1, m2 in zip(copies, results):
        assert weak_message_eq(m1, m2)


def test_get_messages(prepopulated_repo):
    """Retrieves all messages from the repository."""
    messages = prepopulated_repo.get_messages()
    assert len(messages) == 4


def test_get_existing_message(prepopulated_repo):
    """Retrieves a message from the repository."""
    repo = prepopulated_repo
    message = repo.get_messages()[0]
    assert repo.get_message(message.id) == message


def test_get_nonexisting_message(prepopulated_repo):
    """Raises an error when a message is not found."""
    repo = prepopulated_repo
    with raises(MessageNotFoundError):
        repo.get_message(999)


def test_delete_message(prepopulated_repo):
    """Deletes a message from the repository."""
    repo = prepopulated_repo
    message = repo.get_messages()[0]
    repo.delete_message(message.id)

    with raises(MessageNotFoundError):
        repo.get_message(message.id)


def test_delete_messages(prepopulated_repo):
    """Deletes multiple messages from the repository."""
    repo = prepopulated_repo
    messages = repo.get_messages()
    repo.delete_messages(messages[:2])

    assert repo.get_messages() == messages[2:]
