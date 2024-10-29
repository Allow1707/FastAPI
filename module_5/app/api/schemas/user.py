import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    name: str
    role: Optional[]


class ToDoFromDB(ToDoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    created_at: datetime.datetime