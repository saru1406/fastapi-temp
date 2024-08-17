import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default=None):
    """環境変数を取得し、空文字列の場合はNoneを返す"""
    value = os.getenv(key, default)
    return value if value else None


# 環境変数の設定
FRONT_URL = get_env("FRONT_URL")
DB_DATABASE = get_env("DB_DATABASE")
DB_USER = get_env("DB_USER")
DB_PASSWORD = get_env("DB_PASSWORD")
DB_ROOT_PASSWORD = get_env("DB_ROOT_PASSWORD")
SECRET_KEY = get_env("SECRET_KEY")
ALGORITHM = get_env("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = get_env("ACCESS_TOKEN_EXPIRE_MINUTES")
