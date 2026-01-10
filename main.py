from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.post.routes import post_router
from src.db.main import initdb


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server starting...")
    await initdb()
    yield
    print("Server stopping...")


app = FastAPI(title="Blog API", lifespan=lifespan)

app.include_router(post_router)


@app.get("/")
async def home():
    return {"message": "Hello World"}
