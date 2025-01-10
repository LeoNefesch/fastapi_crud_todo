from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from models.models import TodoItem
from storages.db_queries import SQLiteTodoService, TodoService
from storages.db_connection import get_db


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return SQLiteTodoService(db=db, model=TodoItem)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]
