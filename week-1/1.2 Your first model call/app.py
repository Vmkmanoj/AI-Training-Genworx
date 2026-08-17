import os

import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

url = os.getenv("url")


if not url:
    raise ValueError("The 'url' environment variable is missing or not set.")



headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "groq-version": "2024-04-15",
}

while True:
    inp = input("You: ")
    if inp.lower() == "exit":
        break

    payload = {
    "model": "llama-3.3-70b-versatile",
    "input": inp,
    "temperature": 1,
   }

    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    print(data["output"][1]["content"][0]["text"])