from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import get_env
from app.repositories.user_repository import UserRepository
from app.services.user.user_service import UserService


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginUsecase:
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    async def execute(
        self,
        db: Session,
        form_data: OAuth2PasswordRequestForm,
    ) -> Token:
        user = await self.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=int(get_env.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    async def authenticate_user(self, db: Session, email: str, password: str):
        user = await self.user_repository.async_find_user_by_email(db=db, email=email)
        if not user:
            return False
        if not UserService.verify_password(password, user.password):
            return False
        return user

    def create_access_token(
        self, data: dict, expires_delta: Union[timedelta, None] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, get_env.SECRET_KEY, algorithm=get_env.ALGORITHM
        )
        return encoded_jwt
