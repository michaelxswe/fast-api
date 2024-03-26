from datetime import datetime

from pydantic import BaseModel


class UserCreateModel(BaseModel):
    username: str
    password: str


class UserReadModel(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime


class UserUpdateModel(BaseModel):
    username: str | None = None
    password: str | None = None
