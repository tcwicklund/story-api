import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.story import StoryPrompt, StoryResponse

load_dotenv()  # Load .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_story(prompt: StoryPrompt) -> StoryResponse:
    response = client.responses.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo" if preferred
        input=[
            {
                "role": "system",
                "content": f"You are a creative storyteller skilled in {prompt.genre}.",
            },
            {
                "role": "user",
                "content": f"""
             Tell the first section (under 100 words) of an engaging story titled '{prompt.title}'.
             The story should be suitable for a {prompt.reader_age} year old audience.
             End the passage with 3 creative options the user could choose to continue the story.
             """,
            },
        ],
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
    return StoryResponse(
        title=event["title"],
        content=event["content"],
        choices=event["choices"],
        response_id=response.id,
    )


def generate_next_section(prompt: StoryPrompt) -> StoryResponse:
    response = client.responses.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo" if preferred
        input=[
            {
                "role": "user",
                "content": f"Continue the story based on selected option '{prompt.selected_option}' but do not give additional options to continue.",
            },
        ],
        temperature=0.8,
        previous_response_id=prompt.response_id,
        text={
            "format": {
                "type": "json_schema",
                "name": "story",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["title", "content"],
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
    return StoryResponse(
        title=event["title"],
        content=event["content"],
        response_id=response.id,
    )
