from contextlib import asynccontextmanager

from config.settings import Settings
from fastapi import FastAPI

from database.setup import DatabaseManager
from routers import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application")
    app.state.database_manager.setup()
    app.state.database_manager.create_all_tables()
    yield
    app.state.database_manager.drop_all_tables()
    app.state.database_manager.shutdown()
    print("Closing application")


def create_app(settings: Settings):
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings
    app.state.database_manager = DatabaseManager(url=settings.DATABASE_URL)

    app.include_router(user_router.router)

    @app.get("/ping")
    async def status_check():
        return {"ping": "pong"}

    return app
