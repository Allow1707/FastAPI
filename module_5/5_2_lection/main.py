import uvicorn
import uuid
from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

DATABASE_URL = "postgresql+asyncpg://postgres:7793@localhost:5433/fast_api"

database = Database(DATABASE_URL)


class UserCreate(BaseModel):
    """Модель User для валидации исходных данных"""
    name: str
    role: str


class UserReturn(UserCreate):
    """Модель возврата User"""
    id: Optional[int] = None


@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = "INSERT INTO public.user (name, uuid, role) VALUES (:name, :uuid, :role) RETURNING id"
    values = {"name": user.name, "uuid": str(uuid.uuid4()), "role": user.role}
    print(query)
    try:
        user_id = await database.execute(query=query, values=values)
        print(user_id)
        return {**user.model_dump(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {e}")


@app.get("/user/{user_id}", response_model=UserReturn)
async def get_user(user_id: int):
    query = "SELECT * FROM public.user WHERE id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user from database: {e}")
    if result:
        return UserReturn(name=result['name'], role=result['role'], id=result['id'])
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/user/{user_id}", response_model=UserReturn)
async def update_user(user_id: int, user: UserCreate):
    query = "UPDATE public.user SET name = :name, role = :role WHERE id = :user_id"
    values = {"user_id": user_id, "name": user.name, "role": user.role}
    try:
        await database.execute(query=query, values=values)
        return {**user.model_dump(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user in database: {e}")

@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    query = "DELETE FROM public.user WHERE id = :user_id RETURNING id"
    values = {"user_id": user_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete user from database")
    if deleted_rows:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run(app="main:app")
