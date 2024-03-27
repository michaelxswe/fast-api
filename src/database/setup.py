from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.orms import Base


class DatabaseManager:
    def __init__(self, url: str):
        self.url = url

    def setup(self):
        self.engine = create_engine(url=self.url)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_all_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def drop_all_tables(self):
        Base.metadata.drop_all(bind=self.engine)

    def shutdown(self):
        self.engine.dispose()


def get_database_session(request: Request):
    session: Session = request.app.state.database_manager.Session()
    with session.begin():
        yield session
