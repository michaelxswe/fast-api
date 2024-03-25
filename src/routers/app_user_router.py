from database.manager import get_database_session
from dataclasses import asdict
from fastapi import APIRouter, Depends
from models.app_user_model import AppUserCreateModel, AppUserReadModel, AppUserUpdateModel
from services.app_user_service import AppUserService
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1", tags=["App User"])


@router.post("/app-users", response_model=AppUserReadModel, status_code=201)
async def create_app_user(
    data: AppUserCreateModel,
    app_user_service: AppUserService = Depends(),
    session: Session = Depends(get_database_session),
):
    app_user_orm = app_user_service.create_app_user(data=data, session=session)
    session.commit()
    return AppUserReadModel(**asdict(app_user_orm))


@router.get("/app-users/{id}", response_model=AppUserReadModel, status_code=200)
async def get_app_user_by_id(
    id: int, app_user_service: AppUserService = Depends(), session: Session = Depends(get_database_session)
):

    app_user_orm = app_user_service.get_app_user_by_id(id=id, session=session)
    return AppUserReadModel(**asdict(app_user_orm))


@router.patch("/app-users/{id}", response_model=AppUserReadModel, status_code=200)
async def update_app_user_by_id(
    id: int,
    data: AppUserUpdateModel,
    app_user_service: AppUserService = Depends(),
    session: Session = Depends(get_database_session),
):
    with session.begin():
        app_user_orm = app_user_service.update_app_user_by_id(id=id, data=data, session=session)
        return AppUserReadModel(**asdict(app_user_orm))


@router.delete("/app-users/{id}", response_model=None, status_code=200)
async def delete_app_user_by_id(
    id: int, app_user_service: AppUserService = Depends(), session: Session = Depends(get_database_session)
):
    with session.begin():
        app_user_service.delete_app_user_by_id(id=id, session=session)
