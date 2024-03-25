from sqlalchemy.orm import Session

from database.orms import AppUserOrm
from models.app_user_model import AppUserCreateModel, AppUserUpdateModel
from repos.app_user_repo import AppUserRepo
from fastapi import Depends, HTTPException, status


class AppUserService:
    def __init__(self, app_user_repo: AppUserRepo = Depends()):
        self.app_user_repo = app_user_repo

    def create_app_user(self, data: AppUserCreateModel, session: Session) -> AppUserOrm:
        app_user_orm = self.app_user_repo.create_app_user(data=data, session=session)
        return app_user_orm

    def get_app_user_by_id(self, id: int, session: Session) -> AppUserOrm:
        app_user_orm = self.app_user_repo.get_app_user_by_id(id=id, session=session)
        if not app_user_orm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        return app_user_orm

    def update_app_user_by_id(self, id: int, data: AppUserUpdateModel, session: Session) -> AppUserOrm:
        app_user_orm = self.get_app_user_by_id(id=id, session=session)
        return self.app_user_repo.update_app_user(data=data, app_user_orm=app_user_orm, session=session)

    def delete_app_user_by_id(self, id: int, session: Session) -> None:
        app_user = self.get_app_user_by_id(id=id, session=session)
        self.app_user_repo.delete_app_user(app_user=app_user, session=session)
