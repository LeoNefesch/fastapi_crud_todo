from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from conf import get_ekb_time


class TodoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    is_completed: Optional[bool] = False
    created_at: Optional[datetime] = Field(default_factory=get_ekb_time)


class TodoUpdate(BaseModel):
    title: str = Field(..., max_length=100)
    is_completed: bool


class TodoPartialUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    created_at: datetime

    class ConfigDict:
        from_attributes = True
