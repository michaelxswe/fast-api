from dataclasses import asdict
from fastapi import APIRouter, Depends
from models.user_model import UserCreateModel, UserReadModel, UserUpdateModel
from services.user_service import UserService


router = APIRouter(prefix="/api/v1", tags=["User"])


@router.post("/users", response_model=UserReadModel, status_code=201)
async def create_user(
    user_create_model: UserCreateModel,
    user_service: UserService = Depends(),
):
    user = user_service.create_user(user_create_model=user_create_model)
    return UserReadModel(**asdict(user))


@router.get("/users/{id}", response_model=UserReadModel, status_code=200)
async def get_user_by_id(id: int, user_service: UserService = Depends()):
    user = user_service.get_user_by_id(id=id)
    return UserReadModel(**asdict(user))


@router.patch("/users/{id}", response_model=UserReadModel, status_code=200)
async def update_user_by_id(
    id: int,
    user_update_model: UserUpdateModel,
    user_service: UserService = Depends(),
):
    user = user_service.update_user_by_id(id=id, user_update_model=user_update_model)
    return UserReadModel(**asdict(user))


@router.delete("/users/{id}", response_model=None, status_code=200)
async def delete_user_by_id(id: int, user_service: UserService = Depends()):
    user_service.delete_user_by_id(id=id)
