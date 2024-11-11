from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductReturn(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    uuid: str
    created_at: datetime