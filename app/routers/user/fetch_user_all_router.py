from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema
from app.services.user.user_service import UserService
from app.settings.auth import oauth2_scheme

router = APIRouter()


@router.get("/users/", response_model=list[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    userRepository: UserRepository = Depends(UserRepository),
    token: str = Depends(oauth2_scheme),
):
    await UserService.authenticate_user(db=db, token=token)
    users = userRepository.fetch_users(db, skip=skip, limit=limit)
    return users
