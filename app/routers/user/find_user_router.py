from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema
from app.services.user.user_service import UserService
from app.settings.auth import oauth2_scheme

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(UserRepository),
):
    await UserService.authenticate_user(db=db, token=token)
    user = user_repository.find_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
