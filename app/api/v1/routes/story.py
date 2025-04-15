from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_story():
    return {"title": "The Great Adventure", "content": "Once upon a time..."}
