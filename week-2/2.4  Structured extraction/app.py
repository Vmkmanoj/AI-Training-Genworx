
import os 
import time
from dotenv import load_dotenv
from openrouter import OpenRouter
import json

from pydantic import BaseModel


class AIResponse(BaseModel):
    message: str
    success: bool

load_dotenv()


SYSTEM_PROMPT = """
You are an API response generator.

For every user request, return ONLY a valid JSON object with exactly these fields:

{
    "message": "string",
    "success": true
}

Rules:
- "message" must contain the actual answer to the user's question.
- "success" must be a boolean.
- Use true when you can answer the request successfully.
- Use false when you cannot answer the request.
- Do not add any other fields.
- Do not use Markdown code fences.
- Do not add explanations outside the JSON.
- Always return valid JSON.

Example:

User: What is the capital of France?

Response:
{
    "message": "The capital of France is Paris.",
    "success": true
}
"""


api_key = os.getenv("OPENROUTER_API_KEY")

with OpenRouter(api_key=api_key) as client:


    response = client.chat.send(
            model="nvidia/nemotron-nano-9b-v2:free",
            messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": "can you explain python where we are using it , why we are using it",
                    }
                ],
            temperature=0.7,
            
            )


raw  = response.choices[0].message.content

data = json.loads(raw)

result = AIResponse.model_validate(data)

print(result)





