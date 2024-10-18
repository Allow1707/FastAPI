from pydantic import BaseModel

class Authorization(BaseModel):
    """
    username: str
    password: str
    """
    username: str
    password: str