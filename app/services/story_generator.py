from uuid import uuid4
from app.schemas.story import StoryPrompt, StoryResponse
from app.services.section_generator import generate_section


def generate_story(prompt: StoryPrompt) -> StoryResponse:
    story_id = prompt.story_id or str(uuid4())

    # First section starts at order = 1
    section = generate_section(prompt=prompt, story_id=story_id, order=1)

    return StoryResponse(
        story_id=story_id,
        title=prompt.title,
        genre=prompt.genre,
        age=prompt.age,
        grade_level=prompt.grade_level,
        current_section=section,
        choices=section.choices,
    )
