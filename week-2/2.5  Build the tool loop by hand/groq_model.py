import os
import time

from groq import Groq
from dotenv import load_dotenv
from typing import Any, Optional

load_dotenv()


class GroqModel:

    def __init__(self, model: str):
        self.model = model
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(
        self,
        messages: Any,
        temperature: float = 0.1,
        tools: Optional[list] = None,
        tool_choice: Optional[str] = None,
    ):
        """
        Returns the raw Groq ChatCompletion response so callers can
        inspect .choices[0].message and .tool_calls directly.
        """
        kwargs = dict(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

        if tools is not None:
            kwargs["tools"] = tools

        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice

        return self.client.chat.completions.create(**kwargs)
