from typing import List

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def find_user(self, db: Session, user_id: str) -> User:
        return db.query(User).filter(User.id == user_id).first()

    def find_user_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def fetch_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def store_user(self, db: Session, user: dict) -> None:
        db_user = User(email=user["email"], password=user["password"])
        db.add(db_user)

    async def async_find_user_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
