from redis import asyncio as aioredis
from dotenv import load_dotenv

from conf import settings

load_dotenv()


class RedisService(aioredis.Redis):
    def __init__(self, url: str, **kwargs):
        self.url = url
        self._connection_pool = None
        super().__init__(connection_pool=None, **kwargs)

    async def connect(self):
        if not self._connection_pool:
            self._connection_pool = aioredis.ConnectionPool.from_url(self.url, decode_responses=True)
            self.connection_pool = self._connection_pool

    async def disconnect(self):
        if self._connection_pool:
            await self._connection_pool.disconnect()
            self._connection_pool = None


redis_logging = RedisService(settings.REDIS_LOGGING_URL)
redis_caching = RedisService(settings.REDIS_CACHING_URL)
