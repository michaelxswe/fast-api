from config.settings import Settings
from database.setup import DatabaseManager
from fastapi import FastAPI
from fastapi.testclient import TestClient
from setup import create_app
from pytest import fixture
from database.orms import User


@fixture(scope="session")
def app():
    settings = Settings()  # type: ignore
    app = create_app(settings=settings)
    yield app


@fixture(scope="function")
def client(app: FastAPI):
    with TestClient(app=app) as client:
        database_manager: DatabaseManager = app.state.database_manager
        session = database_manager.Session()
        with session.begin():
            session.add(User(username="nick", password="123"))
            session.add(User(username="alex", password="456"))
        yield client
        database_manager.drop_all_tables()
