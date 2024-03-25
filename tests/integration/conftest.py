from config.settings import Settings
from database.manager import DatabaseManager, get_database_session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import create_app
from pytest import fixture
from sqlalchemy.orm import Session
import pytest


@fixture(scope="session")
def app():
    settings = Settings()  # type: ignore
    app = create_app(settings=settings)
    yield app


@fixture(scope="function")
def db_session(app: FastAPI):
    database_manager: DatabaseManager = app.state.database_manager
    connection = database_manager.engine.connect()
    transaction = connection.begin()
    print("generate session")
    session = database_manager.Session(bind=connection)

    def _get_database_session():
        yield session

    app.dependency_overrides[get_database_session] = _get_database_session

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session):
    with TestClient(app=app) as client:
        yield client