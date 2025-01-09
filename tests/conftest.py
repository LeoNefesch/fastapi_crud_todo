from datetime import datetime
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models.models import Base, TodoItem
from routers.todo_items import get_todo_service
from storages.db_connection import get_db
from storages.db_queries import SQLiteTodoService

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def mock_redis_client():
    """Фикстура для мокирования Redis клиента."""
    return mock.AsyncMock()


@pytest.fixture(autouse=True)
def disable_redis_cache(monkeypatch, mock_redis_client):
    """Фикстура для отключения кэширования путем замены redis_client."""
    monkeypatch.setattr("storages.redis.RedisService", mock_redis_client)


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_todo_service] = lambda: SQLiteTodoService(db=test_db, model=TodoItem)

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def get_first_todo_id(client):
    """Фикстура для получения ID первой задачи."""
    response = client.get("/api/todo")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    return data[0]["id"]


todo_data = [
         {"title": "Task 1", "is_completed": False, "created_at": datetime.now().isoformat()},
         {"title": "Task 2", "is_completed": True, "created_at": datetime.now().isoformat()},
         {"title": "Task 3", "is_completed": True, "created_at": datetime.now().isoformat()},
]
