
from fastapi import FastAPI
from src.routers import user

app = FastAPI(title="User API")
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
