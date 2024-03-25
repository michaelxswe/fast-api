from datetime import datetime

from pydantic import BaseModel


class AppUserCreateModel(BaseModel):
    username: str
    password: str


class AppUserReadModel(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime


class AppUserUpdateModel(BaseModel):
    username: str | None = None
    password: str | None = None
