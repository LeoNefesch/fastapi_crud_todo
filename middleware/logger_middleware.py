import json
from redis import asyncio as aioredis
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware

from conf import get_ekb_time
from logs.logs_config import get_logger

logger = get_logger(__name__)


class BaseLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def log(self, request_data):
        """Метод для логирования, должен быть реализован в наследниках."""
        raise NotImplementedError

    async def dispatch(self, request, call_next):
        request_data = {
            "timestamp": get_ekb_time().isoformat(),
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
        }
        background_task = BackgroundTask(self.log, request_data)

        response = await call_next(request)
        response.background = background_task
        return response


class LoggingRedisMiddleware(BaseLoggingMiddleware):
    def __init__(self, app, redis_client: aioredis.Redis):
        super().__init__(app)
        self.redis_client = redis_client

    async def log(self, request_data):
        """Логирование в Redis."""
        await self.redis_client.rpush("http_logs", json.dumps(request_data))
        await self.redis_client.ltrim("http_logs", -100, -1)


class LoggingFileMiddleware(BaseLoggingMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def log(self, request_data):
        """Логирование в файл."""
        logger.info(json.dumps(request_data))
