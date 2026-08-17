import os
import time
from dotenv import load_dotenv
from openrouter import OpenRouter
from openrouter.errors import TooManyRequestsResponseError

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

with OpenRouter(api_key=api_key) as client:
    retries = 3
    delay = 2.0
    for attempt in range(retries):
        try:
            response = client.chat.send(
                model="nvidia/nemotron-nano-9b-v2:free",
                messages=[
                    {
                        "role": "user",
                        "content": "What is the capital of France?",
                    }
                ],
                temperature=0.1,
            )
            print(response.choices[0].message.content)
            print("\nUsage:")
            print(response.usage)
            break
        except TooManyRequestsResponseError as e:
            if attempt < retries - 1:
                print(f"Rate limited (429). Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
                delay *= 2
            else:
                raise