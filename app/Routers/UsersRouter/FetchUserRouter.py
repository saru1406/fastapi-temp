from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.Schemas.UserSchema import UserSchema
from app.Repositories.UserRepository import UserRepository

router = APIRouter()
    
@router.get("/users/", response_model=list[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    userRepository: UserRepository = Depends(UserRepository)
):
    users = userRepository.get_users(db, skip=skip, limit=limit)
    return users
