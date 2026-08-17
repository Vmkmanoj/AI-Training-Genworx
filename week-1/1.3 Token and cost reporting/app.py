import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel


class ChatResponse(BaseModel):
    assistant: str
    input_token: int
    output_tokens: int
    total_tokens: int


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()

url = os.getenv("url")



if not url:
    raise ValueError("The 'url' environment variable is missing or not set.")


headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

conversation = []

conversation_summary = ""


def call_groq(input_data):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "input": input_data,
        "temperature": 0,
    }

    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def summarize_conversation(messages):
    summary_prompt = f"""
    Summarize this conversation.

    Keep only information that is important
    for continuing the conversation later.

    Conversation:
    {messages}
    """

    data = call_groq(summary_prompt)

    return data["output"][1]["content"][0]["text"]


@app.post("/chat",response_model=ChatResponse)
def chat_app(conversation_input: str):

    global conversation_summary

    conversation.append({
        "role": "user",
        "content": conversation_input,
    })

    if len(conversation) > 10:

        old_messages = conversation[:-6]

        recent_messages = conversation[-6:]

        conversation_summary = summarize_conversation(
            old_messages
        )

        conversation.clear()

        conversation.extend(recent_messages)

    context = []

    if conversation_summary:
        context.append({
            "role": "system",
            "content": (
                "Previous conversation summary:\n"
                + conversation_summary
            ),
        })

    context.extend(conversation)

    data = call_groq(context)

    print(data)

    assistant_text = data["output"][1]["content"][0]["text"]

    conversation.extend(data["output"])

    usage = data["usage"]

    return ChatResponse(
        assistant=assistant_text,
        input_token=usage["input_tokens"],
        output_tokens=usage["output_tokens"],
        total_tokens=usage["total_tokens"],
    )