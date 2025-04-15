from openai import OpenAI
from uuid import uuid4
from typing import List, Optional
import os
from dotenv import load_dotenv
import json

from app.schemas.story import StoryPrompt
from app.schemas.section import Section

load_dotenv()  # Load .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(
    prompt: StoryPrompt,
    selected_choice: str = None,
    is_ending: bool = None,
) -> List[dict]:
    role_intro = f"You are a creative and age-appropriate storyteller in the '{prompt.genre}' genre for a reader"
    if prompt.age:
        role_intro += f" who is {prompt.age} years old."
    elif prompt.grade_level:
        role_intro += f" in {prompt.grade_level}."
    else:
        role_intro += "."

    ## if a selected_choice is not provided, we assume it's the first section of the story
    if not selected_choice:
        user_message = f"""Tell the first section (under 300 words) of an engaging story titled '{prompt.title}'. 
            End the passage with 3 creative choices the user could choose to continue the story."""
    ## otherwise, we assume it's a continuation of the story
    ## if the story is not ending, we assume it's a continuation of the story
    elif not is_ending:
        user_message = f"""Continue the story based on the reader's choice: '{selected_choice}'.
            Provide the next section with new choices. Keep it interesting and age-appropriate."""
    ## if the story is ending, we assume it's the last section of the story
    else:
        if is_ending:
            user_message = f"""Finish the story based on the reader's choice: '{selected_choice}'.
                Provide a satisfying conclusion without additional choices."""
    return [
        {"role": "system", "content": role_intro},
        {"role": "user", "content": user_message},
    ]


def generate_section(
    prompt: StoryPrompt,
    story_id: str,
    order: int,
    selected_choice: str = None,
    is_ending: bool = None,
    previous_section_id: str = None,
) -> Section:

    response = client.responses.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo" if preferred
        input=build_prompt(
            prompt,
            selected_choice=selected_choice,
            is_ending=is_ending,
        ),
        temperature=0.8,
        text={
            "format": {
                "type": "json_schema",
                "name": "story",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "choices": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["title", "content", "choices"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        },
        # stream=True,
    )
    # for event in stream:
    # print(event)

    event = json.loads(response.output_text)
    return Section(
        section_id=str(uuid4()),
        story_id=story_id,
        order=order,
        content=event["content"],
        choices=event["choices"],
        selected_choice=selected_choice,
        is_ending=is_ending or False,
        previous_section_id=previous_section_id,
        response_id=response.id,
    )
