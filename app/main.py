import json

from typing import Annotated, Dict
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from pygments.lexer import default

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


@app.post(f"/create_user")
async def create_user_root(body: User) -> User:
    with open(f"app/db/user.json", "r", encoding="utf-8") as f:
        feedback_data: dict = json.loads(f.read())
    index: int = body.id
    feedback_data.update({f"{index}": dict(body)})
    with open(f"app/db/user.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(feedback_data))
    content = dict(body)
    User(**content)
    return User(**content)

def read_jsonl(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line.strip())



@app.get("/get_product/{product_id}")
async def get_product_root(product_id: int) -> dict:
    content: dict = dict()
    for item in read_jsonl('app/db/products.jsonl'):
        if item['product_id'] == product_id:
            content = item
            break
    return content


def check_item_by_filter(item: dict, keyword: str, category: str | None) -> bool:
    content = True
    if keyword not in item['name'].lower():
        content = False
    else:
        if category:
            content = item['category'] == category
    return content


@app.get("/find_product")
async def get_product_root(keyword: str, category: str | None = None, limit: int | None = None) -> list:
    content: list = list()
    for item in read_jsonl('app/db/products.jsonl'):
        if check_item_by_filter(item, keyword, category):
            if limit:
                if len(content) < limit:
                    content.append(item)
                else:
                    break
            else:
                content.append(item)

    return content

@app.get("/headers")
async def get_product_root(request: Request):
    try:
        user_agent: str = request.headers["user-agent"]
        accept_language: str = request.headers["accept-language"]
    except KeyError as e:
        return JSONResponse(content={"message": "BadRequest"}, status_code=400)
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


