from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, Any

from conf import settings
from models.models import Base


class DatabaseConnection(ABC):
    @abstractmethod
    def get_session(self):
        pass


class SQLiteConnection(DatabaseConnection):
    def __init__(self, config: dict):
        self.config = config
        self.engine = create_engine(
            self.config["DATABASE_URL"],
            connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def get_engine(self):
        return self.engine

    def get_session(self) -> Generator[Session, Any, None]:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


config = {
    "DATABASE_URL": settings.DATABASE_URL
}
sqlite_connection = SQLiteConnection(config)


def get_db() -> Generator[Session, None, None]:
    yield from sqlite_connection.get_session()
