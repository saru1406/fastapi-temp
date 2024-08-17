from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.usecase.login.login_usecase import LoginUsecase

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token")
async def login(
    login_usecase: LoginUsecase = Depends(LoginUsecase),
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return await login_usecase.execute(db=db, form_data=form_data)
