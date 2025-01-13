from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Literal

import jwt
from fastapi import APIRouter, Depends, HTTPException, WebSocket, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from src.psi_backend.database.user import User, UserNotFoundError, user_repository

# TODO Replace with env variable from secrets
# Generate with:
# openssl rand -hex 32
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> User | Literal[False]:
    try:
        user = user_repository.get_user_by_username(username)
    except UserNotFoundError:
        return False

    if not pwd_context.verify(password, user.hashed_pwd):
        return False

    return user


def create_access_token(data: dict[Any, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore

    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    try:
        if token_data.username is None:
            raise credentials_exception
        user = user_repository.get_user_by_username(token_data.username)
    except UserNotFoundError:
        raise credentials_exception

    return user


async def validate_websocket(token: str, websocket: WebSocket) -> User:

    if not token:
        await websocket.close(code=1008, reason="Missing token")
        raise HTTPException(status_code=400, detail="Missing token")

    # Validate the token and get the current user
    try:
        user = get_current_user(token)
    except HTTPException as e:
        await websocket.close(code=1008, reason="Invalid token")
        raise e

    if user.id is None:
        await websocket.close(code=1008, reason="Invalid user ID")
        raise HTTPException(status_code=400, detail="Invalid user ID")

    return user


@auth_router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:

    user = authenticate_user(
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/register")
def register_new_user(request: RegisterRequest):

    hashed_pwd = get_password_hash(request.password)

    user = User(username=request.username, email=request.email, hashed_pwd=hashed_pwd)
    try:
        user_repository.add_user(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or user email already exists.",
        )

    return {"message": "User registered successfully"}
