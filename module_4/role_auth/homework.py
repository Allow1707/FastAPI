import jwt
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from secrets import compare_digest

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

app = FastAPI()

# OAuth2PasswordBearer для авторизации по токену
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = None

class AuthData(BaseModel):
    username: str
    password: str

USERS_DATA = [
    User(**{"username": "Alex", "password" :"123", "role": "admin"}),
    User(**{"username": "Valera", "password" :"456", "role": "user"}),
    User(**{"username": "Dany", "password" :"789", "role": "guest"}),
]

def get_user(username: str) -> User | None:
    """Получаем юзера из БД"""
    for user in USERS_DATA:
        if username == user.username:
            return user
    return None

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

def get_sub(token: str = Depends(oauth2_scheme)) -> str:
    """Получаем sub юзера по jwt токен"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/login")
def login_route(user: AuthData):
    """Вводим логин и пароль, чтобы получить jwt токен"""
    username: str = user.username
    password: str = user.password
    user: User | None = get_user(username)
    if user and compare_digest(password, user.password):
        jwt_data: dict = {"sub": username}
        jwt_token: str = create_jwt_token(jwt_data, timedelta(1))
        return {
            "access_token": jwt_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid UserData"
        )

@app.get("/admin")
def admin_route(sub: str = Depends(get_sub)):
    user_data: User = get_user(sub)
    if user_data.role == 'admin':
        return {
            "message": f"Hello {user_data.username}. You Admin!"
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not authorized")

@app.get("/user")
def user_route(sub: str = Depends(get_sub)):
    user_data: User = get_user(sub)
    if user_data.role == 'user':
        return {
            "message": f"Hello {user_data.username}. You User!"
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized")

@app.get("/guest")
def guest_route(sub: str = Depends(get_sub)):
    user_data: User = get_user(sub)
    if user_data.role == 'guest':
        return {
            "message": f"Hello {user_data.username}. You Guest!"
        }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Guest not authorized")





