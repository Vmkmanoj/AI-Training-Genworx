import os

import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

conversation = []

url = os.getenv("url")


headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

while True:

    user_input = input("Enter the user input: ")

    if user_input.lower().strip() == "exit":
        break

   
    conversation.append({
        "role": "user",
        "content": user_input,
    })

    payload = {
        "model": "llama-3.3-70b-versatile",
        "input": conversation,
        "temperature": 0.7,
    }

    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    # Useful while debugging
    if response.status_code != 200:
        print("Status:", response.status_code)
        print("Error:", response.text)
        continue

    data = response.json()

    # Get the generated text
    assistant_text = data["output"][1]["content"][0]["text"]

    print("Assistant:", assistant_text)

    # IMPORTANT:
    # Store Groq's actual output objects
    conversation.extend(data["output"])