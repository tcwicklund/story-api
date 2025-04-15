from fastapi import APIRouter
from app.schemas.story import StoryPrompt, StoryResponse
from app.services.story_generator import generate_story, generate_next_section

router = APIRouter()


@router.post("/", response_model=StoryResponse)
async def create_story(prompt: StoryPrompt):
    return generate_story(prompt)


@router.post("/continue", response_model=StoryResponse)
async def continue_story(prompt: StoryPrompt):
    return generate_next_section(prompt)
