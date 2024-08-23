from fastapi import APIRouter, Depends

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.services.user.user_service import UserService
from sqlalchemy.orm import Session
from app.auth import oauth2_scheme
router = APIRouter()


@router.get("/users/me/", response_model=UserSchema)
async def fetch_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await UserService.fetch_current_user(db=db, token=token)
