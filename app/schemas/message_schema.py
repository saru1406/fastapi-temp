from pydantic import BaseModel


class MessageSchemaBase(BaseModel):
    message: str
