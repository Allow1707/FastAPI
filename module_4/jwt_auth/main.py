import jwt
from datetime import timedelta, datetime
from fastapi import FastAPI, Depends, status, HTTPException, Request
from pydantic import BaseModel

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


class User(BaseModel):
    username: str
    password: str


USERS_DATA = [
    User(**{"username": "admin", "password": "adminpass"})
]


def create_jwt_token(data: dict, expires_delta: timedelta = None) -> str:
    """Функция создания JWT токена"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)  # По умолчанию 15 минут
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_data_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем токен
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


def get_user(username: str) -> User | None:
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None


app = FastAPI()


@app.post("/login")
async def login_root(user_data: User) -> dict:
    if user_data in USERS_DATA:
        token_data = {'sub': user_data.username}
        token = create_jwt_token(token_data, timedelta(1))
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid UserData"
        )


@app.get("/protected_resource")
async def protected_resource_root(request: Request):
    token = request.headers.get('Authorization')
    sub = get_user_data_from_token(token)
    return {"message": f"Hi: {sub}"}
