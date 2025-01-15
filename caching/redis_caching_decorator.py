import json
from functools import wraps
from typing import Callable, TypeVar

from pydantic import TypeAdapter

from schemas.todo import TodoResponse
from storages.redis import redis_caching
from utils.dependencies import TodoServiceDep

T = TypeVar('T')


def cache_result(ttl: int = 60, namespace: str = "todos", key_postfix: str = ""):
    """Декоратор для кэширования ответа FastAPI эндпоинта.
        :param ttl: Время жизни кэша в секундах.
        :param namespace: Пространство имен для ключей в Redis.
        :param key_postfix: Постфикс ключа для кэша (например, 'all' для всех данных)."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            resource_id = kwargs.get("id")
            cache_key = f"{namespace}:{key_postfix if not resource_id else resource_id}"

            if redis_caching and redis_caching.enabled:
                cached_value = await redis_caching.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)

            result = await func(*args, **kwargs)
            if redis_caching and redis_caching.enabled:
                type_adapter = TypeAdapter(list[TodoResponse] if isinstance(result, list) else TodoResponse)
                encoded = type_adapter.dump_json(result).decode("utf-8")
                await redis_caching.set(cache_key, encoded, ex=ttl)

            return result
        return wrapper
    return decorator


def update_cache(ttl: int = 60, namespace: str = "todos", key_postfix: str = "all",
                 update_all: bool = True, update_single: bool = False):
    """Декоратор для обновления кэша после неидемпотентных запросов.
        :param ttl: Время жизни кэша в секундах.
        :param namespace: Пространство имен для ключей в Redis.
        :param key_postfix: Постфикс ключа для кэша (например, 'all' для всех данных).
        :param update_all: Обновить кэш для всех данных.
        :param update_single: Обновить кэш для конкретного объекта."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            if redis_caching and redis_caching.enabled:
                service: TodoServiceDep = kwargs.get('service')

                if update_single and "id" in kwargs:
                    resource_id = kwargs['id']
                    cache_key = f"{namespace}:{resource_id}"
                    type_adapter = TypeAdapter(TodoResponse)
                    encoded_todo = type_adapter.dump_json(result).decode("utf-8")
                    await redis_caching.set(cache_key, encoded_todo, ex=ttl)

                if update_all:
                    cache_key = f"{namespace}:{key_postfix}"
                    todos = service.get_all()
                    type_adapter_all = TypeAdapter(list[TodoResponse])
                    encoded_todos = type_adapter_all.dump_json(todos).decode("utf-8")
                    await redis_caching.set(cache_key, encoded_todos, ex=ttl)

            return result
        return wrapper
    return decorator
