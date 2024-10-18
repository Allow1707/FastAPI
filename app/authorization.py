import json
import time
import uuid
from fastapi import FastAPI, Cookie, Response
from fastapi.responses import JSONResponse
from datetime import datetime

from app.main import user_root
from app.models.authorization_data import Authorization


app = FastAPI()

@app.post("/login")
async def login_root(authorization_data: Authorization, response: Response):
    session_token: str = str(uuid.uuid4())
    user_authorization_data: dict = dict(authorization_data)
    user_authorization_data.update({'session_token': session_token})
    with open("app/db/user_authorization.json", "r", encoding="utf-8") as f:
        users_data: dict = json.loads(f.read())
    if users_data:
        lust_index = int(list(users_data.keys())[-1])
    else:
        lust_index = 0
    users_data[lust_index + 1] = user_authorization_data
    with open("app/db/user_authorization.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(users_data))

    response.set_cookie(key="session_token", value=session_token, httponly=True)
    now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    response.set_cookie(key="lust_vizit", value=now, httponly=True)

# Параметр session_token должен совпадать с key cookie
@app.get("/user")
async def user_root(session_token: str | None = Cookie(default=None)):
    print(1)
    if not session_token:
        return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
    else:
        with open("app/db/user_authorization.json", "r", encoding="utf-8") as f:
            users_data: dict = json.loads(f.read())

        for _, values in users_data.items():
            print(values)
            if values['session_token'] == session_token:
                return values
        return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
