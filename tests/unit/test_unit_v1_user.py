from datetime import datetime
from models.user_model import UserCreateModel, UserUpdateModel
from pytest import fixture
from sqlalchemy.orm import Session
from fastapi import FastAPI
from repos.user_repo import UserRepo
from fastapi.testclient import TestClient
from dataclasses import dataclass


@fixture(scope="function")
def user_repo(app: FastAPI):
    @dataclass
    class User:
        id: int
        username: str
        password: str
        created_at: datetime

    class MockUserRepo:
        def __init__(self):
            self.database = [
                User(
                    id=1,
                    username="alex",
                    password="123",
                    created_at=datetime.utcnow(),
                ),
                User(
                    id=2,
                    username="nick",
                    password="456",
                    created_at=datetime.utcnow(),
                ),
                User(
                    id=3,
                    username="eric",
                    password="789",
                    created_at=datetime.utcnow(),
                ),
            ]

        def create_user(self, user_create_model: UserCreateModel, session: Session) -> User | None:
            if session:
                user = User(
                    id=len(self.database) + 1,
                    username=user_create_model.username,
                    password=user_create_model.password,
                    created_at=datetime.utcnow(),
                )
                self.database.append(user)
                return self.database[-1]

        def get_user_by_id(self, id: int, session: Session) -> User | None:
            print(self.database)
            if session:
                for user in self.database:
                    if user.id == id:
                        return user

                return None

        def update_user(self, user_update_model: UserUpdateModel, user: User, session: Session) -> User | None:
            if session:
                for key, val in user_update_model.model_dump(exclude_none=True).items():
                    setattr(user, key, val)
                return user

        def delete_user(self, user: User, session: Session) -> None:
            if session:
                self.database = [mock_user for mock_user in self.database if mock_user.id != user.id]

    mock_user_repo = MockUserRepo()
    app.dependency_overrides[UserRepo] = lambda: mock_user_repo
    # allows class state to persist throughou the whole test
    yield


def test_create_user(client: TestClient, user_repo):
    print(1)
    data = {"username": "mike", "password": "000"}
    res = client.post("/api/v1/users", json=data)

    assert res.status_code == 201
    assert res.json()["username"] == "mike"
    assert res.json()["password"] == "000"
    assert "id" in res.json()
    assert "created_at" in res.json()


def test_get_user(client: TestClient, user_repo):
    print(2)
    res = client.get("/api/v1/users/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1
    assert res.json()["username"] == "alex"
    assert res.json()["password"] == "123"
    assert "created_at" in res.json()

    res = client.get("/api/v1/users/10")
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}


def test_update_user(client: TestClient, user_repo):
    res = client.patch("/api/v1/users/2", json={"password": "111"})

    assert res.status_code == 200
    assert res.json()["id"] == 2
    assert res.json()["username"] == "nick"
    assert res.json()["password"] == "111"
    assert "created_at" in res.json()


def test_delete_app_user(client: TestClient, user_repo):
    res = client.delete("/api/v1/users/3")
    assert res.status_code == 200
    assert res.json() is None

    res = client.get("/api/v1/users/3")
    assert res.status_code == 404
