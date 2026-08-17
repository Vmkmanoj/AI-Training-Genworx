import os 

import time 

from groq import Groq

from dotenv import load_dotenv

from typing import Any, Iterator

from .base import ModelResponse, ModelInterface, StreamChunk

load_dotenv()

class GroqModel(ModelInterface):
    
    def __init__(self, model: str):
        self.model = model
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )


    def generate(
        self,
        messages: Any,
        temperature: float = 0.1,
    ) -> ModelResponse:
    
        start = time.perf_counter()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

        latency = time.perf_counter() - start

        usage = response.usage
        input_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0

        return ModelResponse(
            content=response.choices[0].message.content or "",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency=latency,
        )


