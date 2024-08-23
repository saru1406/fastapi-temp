from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    email: str


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchema(UserSchemaBase):
    id: str
    password: str
    is_active: bool

    class Config:
        orm_mode = True
