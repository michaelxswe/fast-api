from config.settings import Settings
from database.setup import DatabaseManager
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import create_app
from pytest import fixture
import pytest


@fixture(scope="session")
def app():
    settings = Settings()  # type: ignore
    app = create_app(settings=settings)
    database_manager: DatabaseManager = app.state.database_manager
    database_manager.create_all_tables()
    # populate data
    yield app
    database_manager.drop_all_tables()


@pytest.fixture(scope="function")
def client(app: FastAPI):
    with TestClient(app=app) as client:
        yield client
