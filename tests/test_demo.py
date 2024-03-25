from database.manager import get_database_session
from fastapi.testclient import TestClient
from test import app, engine, SessionLocal
from pytest import fixture
from sqlalchemy.orm import Session
import pytest


@fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    def _get_database_session():
        yield session

    app.dependency_overrides[get_database_session] = _get_database_session

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def create_app_user(client: TestClient):
    data = {"username": "mike", "password": "123"}
    res = client.post("/api/v1/app-users", json=data)
    assert res.status_code == 201
    yield res.json()


def test_delete_app_user(client: TestClient, create_app_user):
    user = create_app_user
    id = user["id"]

    res = client.delete(f"/api/v1/app-users/{id}")
    assert res.status_code == 200
