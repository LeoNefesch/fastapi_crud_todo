import os
from datetime import datetime

from dotenv import load_dotenv
import pytz


load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/todo.db")
    REDIS_LOGGING_URL = os.getenv("REDIS_LOGGING_URL", "redis://localhost:6379/0")
    REDIS_CACHING_URL = os.getenv("REDIS_CACHING_URL", "redis://localhost:6379/1")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    EKB_TZ = pytz.timezone('Asia/Yekaterinburg')


settings = Settings()


def get_ekb_time():
    return datetime.now(settings.EKB_TZ)
