import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.product import database

# Подключение роутов к приложению
from app.api.endpoints.products import products_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app")
