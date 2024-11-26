import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


# не изменяли
class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# не изменяли
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


# Обработчик глобальных исключений, который "ловит" все необработанные исключения
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# добавили непредусмотренное исключение
@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    # симулируем непредусмотренное исключение
    result = 1 / 0
    return {"item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app="main:app")