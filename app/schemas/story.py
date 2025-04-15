from pydantic import BaseModel


class StoryPrompt(BaseModel):
    title: str
    genre: str
    reader_age: str
    response_id: str = None
    selected_option: str = None  # Optional: selected option for continuing the story


class StoryResponse(BaseModel):
    title: str
    content: str
    response_id: str
    choices: list[str] = []  # Optional: list of choices for the user to select from
