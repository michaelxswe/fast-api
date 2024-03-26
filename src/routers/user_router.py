from database.setup import get_database_session
from dataclasses import asdict
from fastapi import APIRouter, Depends
from models.user_model import UserCreateModel, UserReadModel, UserUpdateModel
from services.user_service import UserService
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1", tags=["User"])


@router.post("/users", response_model=UserReadModel, status_code=201)
async def create_user(
    user_create_model: UserCreateModel,
    user_service: UserService = Depends(),
    session: Session = Depends(get_database_session),
):
    with session.begin():
        user = user_service.create_user(user_create_model=user_create_model, session=session)

        return UserReadModel(**asdict(user))


@router.get("/users/{id}", response_model=UserReadModel, status_code=200)
async def get_user_by_id(
    id: int, user_service: UserService = Depends(), session: Session = Depends(get_database_session)
):
    user = user_service.get_user_by_id(id=id, session=session)
    return UserReadModel(**asdict(user))


@router.patch("/users/{id}", response_model=UserReadModel, status_code=200)
async def update_user_by_id(
    id: int,
    user_update_model: UserUpdateModel,
    user_service: UserService = Depends(),
    session: Session = Depends(get_database_session),
):
    with session.begin():
        user = user_service.update_user_by_id(id=id, user_update_model=user_update_model, session=session)
        return UserReadModel(**asdict(user))


@router.delete("/users/{id}", response_model=None, status_code=200)
async def delete_user_by_id(
    id: int, user_service: UserService = Depends(), session: Session = Depends(get_database_session)
):
    with session.begin():
        user_service.delete_user_by_id(id=id, session=session)
