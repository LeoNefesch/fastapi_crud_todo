import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from conf import settings
from middleware.logger_middleware import LoggingFileMiddleware, LoggingRedisMiddleware
from routers.todo_items import router
from storages.redis import redis_caching, redis_logging

load_dotenv()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Подключение к Redis при запуске приложения и закрытие соединений с Redis при завершении работы приложения"""
    await redis_logging.connect()
    await redis_caching.connect()
    yield
    await redis_logging.disconnect()
    await redis_caching.disconnect()

app = FastAPI(title="ToDoApp", lifespan=app_lifespan)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error: {exc}"},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )


app.add_middleware(LoggingRedisMiddleware, redis_client=redis_logging)
app.add_middleware(LoggingFileMiddleware)
app.include_router(router)

if __name__ == "__main__" and os.getenv("ENVIRONMENT", "development") == "development":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, workers=4)
