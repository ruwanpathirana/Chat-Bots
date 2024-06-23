from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

class Item(BaseModel):
    number1: float
    number2: float

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.post("/sum")
async def sum(item: Item):
    return {"result": item.number1 + item.number2}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port = 8000, reload = True)