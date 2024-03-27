from sqlalchemy.orm import Session
from database.orms import User
from database.setup import get_database_session
from models.user_model import UserCreateModel, UserUpdateModel
from repos.user_repo import UserRepo
from fastapi import Depends, HTTPException, status


class UserService:
    def __init__(self, user_repo: UserRepo = Depends(), session: Session = Depends(get_database_session)):
        self.user_repo = user_repo
        self.session = session

    def create_user(self, user_create_model: UserCreateModel) -> User:
        user = self.user_repo.create_user(user_create_model=user_create_model, session=self.session)
        return user

    def get_user_by_id(self, id: int) -> User:
        user = self.user_repo.get_user_by_id(id=id, session=self.session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user

    def update_user_by_id(self, id: int, user_update_model: UserUpdateModel) -> User:
        user = self.get_user_by_id(id=id)

        return self.user_repo.update_user(user_update_model=user_update_model, user=user, session=self.session)

    def delete_user_by_id(self, id: int) -> None:
        user = self.get_user_by_id(id=id)
        self.user_repo.delete_user(user=user, session=self.session)
