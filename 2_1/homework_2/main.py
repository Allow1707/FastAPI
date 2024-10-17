from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CalculateBody(BaseModel):
    num_1: float
    num_2: float

@app.post("/calculate")
async def root(body: CalculateBody):
    content: dict = {
        "sum": body.num_1 + body.num_2
    }
    return content