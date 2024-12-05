from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator, conint, EmailStr, constr



app = FastAPI()
#
# # кастомный обработчик исключения для всех HTTPException
# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": exc.detail},
#     )
#

# кастомный обработчик исключения для RequestValidationError (Pydantic validation errors - 422 Unprocessable Entity)
@app.exception_handler(RequestValidationError)
async def custom_request_validation_exception_handler(request, exc):
    error_message = ""
    for i, error in enumerate(exc.errors()):
        error_message += f"{i}) {'->'.join(error['loc'])}: {error['msg']}\n"

    return JSONResponse(
        status_code=400,
        content={"message": "BadRequest", "errors": error_message},

        # content={"message": "BadRequest", "errors": f"{'->'.join(exc.errors().loc)}: {exc.errors().msg}"},
    )

class User(BaseModel):
    username: str
    age: conint(ge=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Union[float, None] = None


@app.post("/create_user/")
async def create_user(item: User):
    return {"message": "User created successfully", "item": item}

if __name__ == "__main__":
    uvicorn.run(app="homework:app")