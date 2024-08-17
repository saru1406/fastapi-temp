from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.message_schema import MessageSchemaBase
from app.schemas.user_schema import UserSchemaCreate
from app.usecase.user.store_user_usecase import StoreUserUsecase

router = APIRouter()


@router.post("/users/", response_model=MessageSchemaBase)
def create_user(
    user: UserSchemaCreate,
    db: Session = Depends(get_db),
    userRepository: UserRepository = Depends(UserRepository),
    store_user_usecase: StoreUserUsecase = Depends(StoreUserUsecase),
):
    db_user = userRepository.find_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    store_user_usecase.execute(db=db, user=user)
    db.commit()
    return {"message": "successful"}
