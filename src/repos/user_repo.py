from database.orms import User
from models.user_model import UserCreateModel, UserUpdateModel
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepo:
    def create_user(self, user_create_model: UserCreateModel, session: Session) -> User:
        user = User(**user_create_model.model_dump())
        session.add(user)
        session.flush()
        return user

    def get_user_by_id(self, id: int, session: Session) -> User | None:
        query = select(User).where(User.id == id)
        result = session.execute(query)
        user = result.scalar()
        return user

    def update_user(self, user_update_model: UserUpdateModel, user: User, session: Session) -> User:
        for key, val in user_update_model.model_dump(exclude_none=True).items():
            setattr(user, key, val)

        session.flush()
        return user

    def delete_user(self, user: User, session: Session) -> None:
        session.delete(user)
