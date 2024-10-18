from pydantic import BaseModel

class User(BaseModel):
    """
    id: int
    name: str
    age: int
    """
    id: int
    name: str
    age: int
    is_subscription: bool = False