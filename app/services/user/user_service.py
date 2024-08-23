from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import get_env
from app.emun.user_status import UserStatus
from app.models.user import User
from app.repositories.user_repository import UserRepository


class TokenData(BaseModel):
    user_email: Union[str, None] = None


class UserService:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(form_password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(form_password, hashed_password)

    @staticmethod
    async def fetch_current_user(db: Session, token: str):
        user_email = UserService.decode_token(token)
        token_data = TokenData(user_email=user_email)
        user_repository = UserRepository()
        user = await user_repository.async_find_user_by_email(
            db=db, email=token_data.user_email
        )
        UserService.check_user(user=user)
        UserService.check_active(user=user)
        return user

    @staticmethod
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(
                token, get_env.SECRET_KEY, algorithms=[get_env.ALGORITHM]
            )
            return payload.get("sub")
        except InvalidTokenError:
            raise UserService.credentials_exception

    @staticmethod
    def check_user(user: Union[User, None]) -> None:
        if user is None:
            raise UserService.credentials_exception

    @staticmethod
    def check_active(user: User) -> None:
        if user.is_active == UserStatus.NOTACTIVE:
            raise UserService.credentials_exception
