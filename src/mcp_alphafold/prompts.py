import os

from pydantic import BaseModel
from typing import Optional


class PromptArgs(BaseModel):
    ALPHAFOLD_TOOLS: str
    ONE_SHOT_EXAMPLES: str


def load_prompt(args: PromptArgs) -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.md")
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()
    return prompt_template.format(**args.dict())
