from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema, UserSchemaCreate

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(
    user: UserSchemaCreate,
    db: Session = Depends(get_db),
    userRepository: UserRepository = Depends(UserRepository),
):
    db_user = userRepository.find_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return userRepository.store_user(db=db, user=user)
