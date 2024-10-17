import json

from fastapi import FastAPI
from app.models.user import User
from app.models.calculate import CalculateBody
from app.models.feedback import Feedback

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/calculate")
async def root(body: CalculateBody):
    content: dict = {
        "sum": body.num_1 + body.num_2
    }
    return content


@app.get("/users/{user_id}")
def read_user(user_id: str):
    with open(f"app/db/user.json", "r", encoding="utf-8") as f:
        users_data: dict = json.loads(f.read())
    if user_id in users_data:
        return users_data[user_id]
    return {"error": "User not found"}


@app.post("/user")
async def user_root(body: User):
    body_dict: dict = dict(body)
    if body.age >= 18:
        body_dict.update({'is_adult': True})
    else:
        body_dict.update({'is_adult': False})
    return body_dict


@app.post("/feedback")
async def feedback_root(body: Feedback):
    with open(f"app/db/feedback.json", "r", encoding="utf-8") as f:
        feedback_data: dict = json.loads(f.read())
    index: int = len(feedback_data)
    feedback_data.update({f"{len(feedback_data)}": dict(body)})
    with open(f"app/db/feedback.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(feedback_data))
    content: dict = {"message": f"Feedback received. Thank you, {body.name}!"}
    return content


@app.get("/feedback")
async def get_feedback_root(limit: int = 10):
    with open(f"app/db/feedback.json", "r", encoding="utf-8") as f:
        feedback_data: dict = json.loads(f.read())
    content = dict(list(feedback_data.items())[:limit])
    return content
