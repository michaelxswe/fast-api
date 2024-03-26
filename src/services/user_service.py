from sqlalchemy.orm import Session

from database.orms import User
from models.user_model import UserCreateModel, UserUpdateModel
from repos.user_repo import UserRepo
from fastapi import Depends, HTTPException, status


class UserService:
    def __init__(self, user_repo: UserRepo = Depends()):
        self.user_repo = user_repo

    def create_user(self, user_create_model: UserCreateModel, session: Session) -> User:
        user = self.user_repo.create_user(user_create_model=user_create_model, session=session)
        return user

    def get_user_by_id(self, id: int, session: Session) -> User:
        user = self.user_repo.get_user_by_id(id=id, session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user

    def update_user_by_id(self, id: int, user_update_model: UserUpdateModel, session: Session) -> User:
        user = self.get_user_by_id(id=id, session=session)
        return self.user_repo.update_user(user_update_model=user_update_model, user=user, session=session)

    def delete_user_by_id(self, id: int, session: Session) -> None:
        user = self.get_user_by_id(id=id, session=session)
        self.user_repo.delete_user(user=user, session=session)
