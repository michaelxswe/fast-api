from database.orms import AppUserOrm
from models.app_user_model import AppUserCreateModel, AppUserUpdateModel
from sqlalchemy import select
from sqlalchemy.orm import Session


class AppUserRepo:
    def create_app_user(self, data: AppUserCreateModel, session: Session) -> AppUserOrm:
        app_user_orm = AppUserOrm(**data.model_dump())
        session.add(app_user_orm)
        session.flush()
        session.refresh(app_user_orm)
        return app_user_orm

    def get_app_user_by_id(self, id: int, session: Session) -> AppUserOrm | None:
        query = select(AppUserOrm).where(AppUserOrm.id == id)
        result = session.execute(query)
        app_user_orm = result.scalar()
        return app_user_orm

    def update_app_user(self, data: AppUserUpdateModel, app_user_orm: AppUserOrm, session: Session) -> AppUserOrm:
        for key, val in data.model_dump(exclude_none=True).items():
            setattr(app_user_orm, key, val)

        session.flush()
        session.refresh(app_user_orm)
        return app_user_orm

    def delete_app_user(self, app_user: AppUserOrm, session: Session) -> None:
        session.delete(app_user)
