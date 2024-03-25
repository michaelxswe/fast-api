from contextlib import asynccontextmanager
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, sessionmaker, Session
from fastapi import Depends, FastAPI, Request
from pydantic_settings import BaseSettings


class Base(DeclarativeBase, MappedAsDataclass):
    pass

engine = create_engine(url = "postgresql+psycopg2://postgres:0000@localhost:5432/db")
SessionLocal = sessionmaker(bind=engine)

class AppUserOrm(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(length=25), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(length=25))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), init=False)

class AppUserCreateModel(BaseModel):
    username: str
    password: str


class AppUserReadModel(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime


def get_database_session():
    try:
        session: Session = SessionLocal()
        yield session
    finally:
        session.close()
        
Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/api/v1/app-users", status_code=201)
def add_add_user(data: AppUserCreateModel, session: Session = Depends(get_database_session)):
    app_user_orm = AppUserOrm(**data.model_dump())
    session.add(app_user_orm)
    session.flush()
    session.refresh(app_user_orm)
    session.commit()
    return app_user_orm


@app.delete("/api/v1/app-users/{id}", status_code=200)
async def delete_app_user_by_id(id: int, session: Session = Depends(get_database_session)):
    with session.begin():
        query = select(AppUserOrm).where(AppUserOrm.id == id)
        result = session.execute(query)
        app_user_orm = result.scalar()
        session.delete(app_user_orm)
