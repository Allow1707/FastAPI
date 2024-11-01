import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    role: str = 'guest'


class UserFromDB(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime