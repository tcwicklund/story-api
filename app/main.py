from fastapi import FastAPI
from app.api.v1.routes import story

app = FastAPI()

app.include_router(story.router, prefix="/api/v1/story", tags=["Story"])


@app.get("/")
async def root():
    return {"message": "FastAPI backend is alive!"}
