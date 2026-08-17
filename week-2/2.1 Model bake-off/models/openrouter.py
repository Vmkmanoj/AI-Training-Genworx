import os 
import time

from dotenv import load_dotenv
from openrouter import OpenRouter

from .base import ModelInterface , ModelResponse



load_dotenv()

class OpenRouterModel(ModelInterface):
    
    def __init__(self,model : str):
        self.model  = model
        self.client = OpenRouter(
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )


    def generate(self,
        messages: list[dict],
        temperature: float = 0.1,
    ) -> ModelResponse:
    
        start = time.perf_counter()

        response = self.client.chat.send(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

        latency = time.perf_counter() - start

        usage = response.usage

        return ModelResponse(
            content=response.choices[0].message.content,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            latency=latency,
        )

    
        



