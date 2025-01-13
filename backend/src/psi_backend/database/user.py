from __future__ import annotations

from typing import Optional, Sequence

from attrs import define
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field  # type: ignore
from sqlmodel import Session, SQLModel, select

from src.psi_backend.database.db import engine


class User(SQLModel, table=True):
    """User on the platform."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)
    hashed_pwd: str = Field(nullable=False)


class UserNotFoundError(Exception):
    """Raised when an User is not found."""


class IncorrectCredentialsError(Exception):
    """Raised when User could not be authenticated"""


@define
class UserRepository:
    """An abstraction over the database for Users."""

    engine: Engine

    def add_user(self, user: User) -> int:
        """Add user to database."""
        with Session(self.engine) as session:
            try:
                session.add(user)
                session.commit()
                if user.id is None:
                    raise ValueError("User ID cannot be None")
            except IntegrityError as e:
                session.rollback()
                if "UNIQUE constraint failed" in str(e.orig):
                    raise ValueError("User with this email or username already exists")
                else:
                    raise
            return user.id

    def delete_user(self, user_id: int) -> None:
        """Deletes a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(User, user_id)
            if msg is None:
                raise UserNotFoundError(f"User with id {user_id} not found")

            session.delete(msg)
            session.commit()

    def get_users(self) -> Sequence[User]:
        """Get all users from the database."""
        with Session(self.engine) as session:
            users = session.exec(select(User)).all()
            return users

    def get_user(self, user_id: int) -> User:
        """Get a user from the database."""
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if user is None:
                raise UserNotFoundError(f"User with id {user_id} not found")
            return user

    def get_user_by_username(self, username: str) -> User:
        """Get a user from the database by username."""
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.username == username)).first()
            if user is None:
                raise UserNotFoundError(f"User with username {username} not found")
            return user


user_repository = UserRepository(engine)
