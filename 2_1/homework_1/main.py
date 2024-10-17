from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
@app.get("/")
async def root():
    # Класс для возвращения файлов
    return FileResponse("2_1/homework/index.html")