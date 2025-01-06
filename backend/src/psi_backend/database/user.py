from __future__ import annotations
from datetime import datetime
from sqlalchemy import Engine
from sqlmodel import Field, SQLModel, Session, create_engine, select
from attrs import define
from typing import Optional
import os

from src.psi_backend.database.db import engine


class User(SQLModel, table=True):
    """User on the platform."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    hashed_pwd: str = Field(nullable=False)


class UserNotFoundError(Exception):
    """Raised when an User is not found."""


class IncorrectCredentialsError(Exception):
    """Raised when User could not be authenticated"""


@define
class UserRepository:
    """An abstraction over the database for Users."""

    engine: Engine

    def add_user(self, user: User) -> None:
        """Add user to database."""
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def delete_user(self: int, user_id: int) -> None:
        """Deletes a message from the database."""
        with Session(self.engine) as session:
            msg = session.get(User, user_id)
            if msg is None:
                raise UserNotFoundError(f"User with id {user_id} not found")

            session.delete(msg)
            session.commit()

    def get_users(self) -> list[User]:
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
