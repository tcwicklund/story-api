from pydantic import BaseModel
from typing import Optional, List


class Section(BaseModel):
    section_id: str
    story_id: str
    order: int
    content: str
    choices: List[str]
    selected_choice: Optional[str] = None
    is_ending: bool = False
    response_id: Optional[str] = None
    previous_section_id: Optional[str] = None
