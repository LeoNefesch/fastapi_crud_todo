import json
from functools import wraps
from typing import Callable, TypeVar

from pydantic import TypeAdapter

from schemas.todo import TodoResponse
from storages.redis import redis_caching


T = TypeVar('T')


def cache_result(ttl: int = 60, namespace: str = "todos", key_postfix: str = ""):
    """Декоратор для кэширования ответа FastAPI эндпоинта.
        :param ttl: Время жизни кэша в секундах.
        :param namespace: Пространство имен для ключей в Redis.
        :param key_postfix: Постфикс ключа для кэша (например, 'all' для всех данных)."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if key_postfix:
                cache_key = f"{namespace}:{key_postfix}"
            else:
                resource_id = kwargs.get('id')
                cache_key = f"{namespace}:{resource_id}"

            if redis_caching:
                cached_value = await redis_caching.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)

            result = await func(*args, **kwargs)

            if redis_caching:
                if isinstance(result, list):
                    type_adapter = TypeAdapter(list[TodoResponse])
                else:
                    type_adapter = TypeAdapter(TodoResponse)
                encoded = type_adapter.dump_json(result).decode("utf-8")
                await redis_caching.set(cache_key, encoded, ex=ttl)

            return result
        return wrapper
    return decorator
