import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    description: str
    completed: bool | None = False


class ToDoFromDB(ToDoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    created_at: datetime.datetime