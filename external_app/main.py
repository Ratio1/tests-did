import os
from fastapi import FastAPI, Request

print(os.environ) 

app = FastAPI()

@app.post("/echo")
async def echo(request: Request):
    data = await request.json()
    return {"echo": data}