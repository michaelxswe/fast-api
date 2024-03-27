from config.settings import Settings
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import create_app
from pytest import fixture
from database.setup import get_database_session


@fixture(scope="session")
def app():
    def _get_database_session():
        return True

    settings = Settings(ENV="test", DATABASE_URL="test")  # type: ignore
    app = create_app(settings=settings)
    app.dependency_overrides[get_database_session] = _get_database_session
    yield app


@fixture(scope="session")
def client(app: FastAPI):
    client = TestClient(app=app)
    yield client
