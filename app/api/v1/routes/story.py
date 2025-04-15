from fastapi import APIRouter
from app.schemas.story import StoryPrompt, StoryResponse
from app.services.story_generator import generate_story

router = APIRouter()


@router.post("/", response_model=StoryResponse)
async def create_story(prompt: StoryPrompt):
    return generate_story(prompt)
