import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchemaCreate
from app.services.user.user_service import UserService


class StoreUserUsecase:
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    def execute(self, db: Session, user: UserSchemaCreate):
        user_dict = self.create_user_dict(user=user)
        self.user_repository.store_user(db=db, user=user_dict)

    def create_user_dict(self, user: UserSchemaCreate):
        hash_password = UserService.get_password_hash(password=user.password)
        return {"email": user.email, "password": hash_password}
