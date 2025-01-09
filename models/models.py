from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

from conf import get_ekb_time


Base = declarative_base()


class TodoItem(Base):
    __tablename__ = "todo_item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_ekb_time)
