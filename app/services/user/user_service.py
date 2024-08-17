from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext


class UserService:

    @staticmethod
    def get_password_hash(password) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
