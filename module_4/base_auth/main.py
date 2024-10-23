from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest

app = FastAPI()
security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str


USER_DATA: list = [User(**{"username": "user1", "password": "pass1"}),
                   User(**{"username": "user2", "password": "pass2"})]


def get_user_from_db(username: str):
    """Получаем данные из БД"""
    for user in USER_DATA:
        if user.username == username:
            print(user)
            return user
    return None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Функция авторизации"""
    user = get_user_from_db(credentials.username)
    if user is None or not compare_digest(user.password, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    return user

@app.get("/login")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome!", "user_info": user}