from pydantic import BaseModel

class CalculateBody(BaseModel):
    num_1: float
    num_2: float