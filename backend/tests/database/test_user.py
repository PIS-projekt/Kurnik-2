from __future__ import annotations
import pytest
from sqlmodel import create_engine, SQLModel
from sqlalchemy import Engine

from src.psi_backend.database.user import (
    User,
    UserRepository,
    UserNotFoundError,
)


# In-memory SQLite database for testing
@pytest.fixture(scope="function")
def engine() -> Engine:
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(test_engine)
    return test_engine


@pytest.fixture(scope="function")
def user_repo(engine: Engine) -> UserRepository:
    return UserRepository(engine)


def test_add_user(user_repo: UserRepository) -> None:
    user = User(
        username="testuser", email="test@example.com", hashed_pwd="hashedpwd123"
    )
    user_repo.add_user(user)

    assert user_repo.get_user_by_username("testuser") is not None


def test_delete_user(user_repo: UserRepository) -> None:
    user = User(
        username="testuser", email="test@example.com", hashed_pwd="hashedpwd123"
    )
    new_user_id = user_repo.add_user(user)

    user_repo.delete_user(new_user_id)

    with pytest.raises(UserNotFoundError, match="User with id 1 not found"):
        user_repo.get_user(new_user_id)


def test_delete_nonexistent_user(user_repo: UserRepository) -> None:
    with pytest.raises(UserNotFoundError, match="User with id 999 not found"):
        user_repo.delete_user(999)


def test_get_users(user_repo: UserRepository) -> None:
    user1 = User(username="user1", email="user1@example.com", hashed_pwd="hashedpwd1")
    user2 = User(username="user2", email="user2@example.com", hashed_pwd="hashedpwd2")
    user_repo.add_user(user1)
    user_repo.add_user(user2)

    users = user_repo.get_users()
    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"


def test_get_user(user_repo: UserRepository) -> None:
    user = User(
        username="testuser", email="test@example.com", hashed_pwd="hashedpwd123"
    )
    user_repo.add_user(user)

    assert user.id is not None
    db_user = user_repo.get_user(user.id)
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"


def test_get_user_nonexistent(user_repo: UserRepository) -> None:
    with pytest.raises(UserNotFoundError, match="User with id 999 not found"):
        user_repo.get_user(999)


def test_get_user_by_username(user_repo: UserRepository) -> None:
    user = User(
        username="testuser", email="test@example.com", hashed_pwd="hashedpwd123"
    )
    user_repo.add_user(user)

    db_user = user_repo.get_user_by_username("testuser")
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"


def test_get_user_by_username_nonexistent(user_repo: UserRepository) -> None:
    with pytest.raises(
        UserNotFoundError, match="User with username nonexistentuser not found"
    ):
        user_repo.get_user_by_username("nonexistentuser")


def test_add_user_duplicate_username(user_repo: UserRepository) -> None:
    user1 = User(
        username="testuser", email="test1@example.com", hashed_pwd="hashedpwd123"
    )
    user2 = User(
        username="testuser", email="test2@example.com", hashed_pwd="hashedpwd123"
    )
    user_repo.add_user(user1)

    with pytest.raises(
        ValueError, match="User with this email or username already exists"
    ):
        user_repo.add_user(user2)
