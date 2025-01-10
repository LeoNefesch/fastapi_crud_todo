from typing import Any

from fastapi import APIRouter, HTTPException

from caching.redis_caching_decorator import cache_result
from schemas.todo import TodoCreate, TodoPartialUpdate, TodoResponse, TodoUpdate
from storages.redis import redis_caching
from utils.dependencies import TodoServiceDep

router = APIRouter(prefix="/api/todo", tags=["todos"])


def get_or_404(entity: Any) -> Any:
    if not entity:
        raise HTTPException(status_code=404, detail="Todo not found")
    return entity


@router.post("", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate, service: TodoServiceDep):
    """Создание задачи."""
    return service.create(todo)


@router.get("", response_model=list[TodoResponse])
@cache_result(ttl=120, namespace="todos", key_postfix="all")
async def get_todos(service: TodoServiceDep):
    """Получение списка всех задач с кэшированием."""
    return service.get_all()


@router.get("/{id}", response_model=TodoResponse)
@cache_result(ttl=120, namespace="todos")
async def get_todo(id: int, service: TodoServiceDep):
    """Получение задачи по ID с кэшированием."""
    todo = service.get_by_id(id)
    return get_or_404(todo)


@router.patch("/{id}", response_model=TodoResponse)
async def patch_todo(id: int, todo: TodoPartialUpdate, service: TodoServiceDep):
    """Частичное обновление задачи по ID."""
    updated_todo = service.update_fields(id, todo.model_dump(exclude_unset=True))
    return get_or_404(updated_todo)


@router.put("/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo: TodoUpdate, service: TodoServiceDep):
    """Полное обновление задачи по ID."""
    updated_todo = service.update_fields(id, todo.model_dump())
    return get_or_404(updated_todo)


@router.delete("/{id}", status_code=204)
async def delete_todo(id: int, service: TodoServiceDep):
    """Удаление задачи по ID."""
    success = service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    cache_key = f"todos:{id}"
    if redis_caching and redis_caching.enabled:
        await redis_caching.delete(cache_key)
    return {"message": "Todo deleted successfully"}
