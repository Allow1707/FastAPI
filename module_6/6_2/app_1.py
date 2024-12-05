
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator

app = FastAPI()

# кастомный обработчик исключения для всех HTTPException
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

# кастомный обработчик исключения для RequestValidationError (Pydantic validation errors - 422 Unprocessable Entity)
@app.exception_handler(RequestValidationError)
async def custom_request_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": "Custom Request Validation Error", "errors": exc.errors()},
    )

class Item(BaseModel):
    name: str
    price: float

    @validator("price")
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise HTTPException(status_code=400, detail="Price must be non-negative")
        return value

@app.post("/items/")
async def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}

if __name__ == "__main__":
    uvicorn.run(app="app_1:app")