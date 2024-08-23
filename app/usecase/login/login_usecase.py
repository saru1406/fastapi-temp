from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.emun.user_status import UserStatus
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.token_schema import TokenSchema
from app.services.user.user_service import UserService
from app.settings import env


class LoginUsecase:
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    async def execute(
        self,
        db: Session,
        form_data: OAuth2PasswordRequestForm,
    ) -> TokenSchema:
        user = await self.authenticate_user(
            db=db, form_email=form_data.username, form_password=form_data.password
        )
        access_token_expires = self.token_expires()
        access_token = self.create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires,
        )
        return TokenSchema(access_token=access_token, token_type="bearer")

    async def authenticate_user(
        self, db: Session, form_email: str, form_password: str
    ) -> User:
        user = await self.user_repository.async_find_user_by_email(
            db=db, email=form_email
        )
        self.check_user(user=user)
        self.check_password(form_password=form_password, user_password=user.password)
        self.check_active(user=user)
        return user

    def check_user(self, user: Union[None, User]) -> None:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証に失敗しました。",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def check_password(self, form_password: str, user_password: str) -> None:
        if not UserService.verify_password(form_password, user_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証に失敗しました。",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def check_active(self, user: User) -> None:
        if user.is_active == UserStatus.NOTACTIVE:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効なアカウントです。",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def create_access_token(
        self, data: dict[str, str], expires_delta: Union[timedelta, None] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)
        return encoded_jwt

    def token_expires(self) -> timedelta:
        return timedelta(minutes=int(env.ACCESS_TOKEN_EXPIRE_MINUTES))
