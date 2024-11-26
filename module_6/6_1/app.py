import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_details: str


class BadRequest(HTTPException):
    def __init__(self, detail: str = "BadRequest", status_code: int = 400, message = ""):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


class Forbidden(HTTPException):
    def __init__(self, detail: str = "Forbidden", status_code: int = 403, message = ""):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


@app.exception_handler(BadRequest)
async def bad_request_handler(request: Request, exc: BadRequest):
    error = jsonable_encoder(
        CustomExceptionModel(status_code=exc.status_code, er_message=exc.message, er_details=exc.detail))
    return JSONResponse(status_code=exc.status_code, content=error)

@app.exception_handler(Forbidden)
async def forbidden_handler(request: Request, exc: Forbidden):
    error = jsonable_encoder(
        CustomExceptionModel(status_code=exc.status_code, er_message=exc.message, er_details=exc.detail))
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error = jsonable_encoder(
        CustomExceptionModel(status_code=500, er_message="", er_details="InternalError"))
    return JSONResponse(status_code=500, content=error)


@app.get("/items/{item_id}/")
async def get_item_route(item_id: int):
    # симулируем непредусмотренное исключение
    if item_id == 42:
        raise BadRequest()
    elif item_id == 52:
        raise Forbidden()
    return {"item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app="app:app")
