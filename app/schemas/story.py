from pydantic import BaseModel
from typing import Optional
from app.schemas.section import Section


class StoryBase(BaseModel):
    title: str
    genre: str
    age: Optional[int] = None
    grade_level: Optional[int] = None


class StoryPrompt(StoryBase):
    story_id: Optional[str] = None  # for continuations
    latest_section: Optional[Section] = None  # for continuations


class StoryResponse(StoryBase):
    story_id: str
    current_section: Section
    choices: list[str]
