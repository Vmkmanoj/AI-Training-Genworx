import httpx
import os
import json

from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()

url = os.getenv("URL")
api_key = os.getenv("GROQ_API_KEY")

INPUT_PRICE = 0.075
OUTPUT_PRICE = 0.30

if not url:
    raise ValueError("Environment variable 'URL' is not set")

if not api_key:
    raise ValueError("Environment variable 'GROQ_API_KEY' is not set")


conversation = []

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

def build_context(
    summary: str,
    conversation: list,
    recent_count: int = 10
):

    recent_messages = conversation[-recent_count:]

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    if summary:
        messages.append({
            "role": "system",
            "content": f"""
Conversation summary:

{summary}
"""
        })

    messages.extend(recent_messages)

    return messages


def summary_convertion(messages: list) -> str:

    conversation_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in messages
    )

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "system",
                "content": """
                Summarize this conversation.

                Keep important:
                - user facts
                - preferences
                - goals
                - decisions
                - important technical context

                Do not include unnecessary conversation.
                """
            },
            {
                "role": "user",
                "content": conversation_text
            }
        ],
        "temperature": 0.2,
        "stream": False,
    }

    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


# def summary_convertion(conversation: list) -> str:

#     summary = ""
#     for message in conversation:
#         summary += message["content"]


#     payload={
#         "model": "openai/gpt-oss-20b",
#         "messages": [
#             {
#                 "role": "system",
#                 "content": "Summarize this conversation"
#             },
#             {
#                 "role": "user",
#                 "content": summary
#             }
#         ],
#         "temperature": 0.7,
#         "stream": False,
#     }

#     response = httpx.post(url, headers=headers, json=payload, timeout=30)

#     summary = response.json()["choices"][0]["message"]["content"]

#     return summary


def calculate_cost(input_tokens: int, output_tokens: int):

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_PRICE

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_PRICE

    return input_cost + output_cost


total_cost = 0
summary = ""


while True:

    user_inp = input("You : ")

    if user_inp.lower() == "exit":
        break

    conversation.append({
        "role": "user",
        "content": user_inp
    })

    # --------------------------------
    # Create summary if history grows
    # --------------------------------

    if len(conversation) > 10:

        summary = summary_convertion(
            conversation[:-10]
        )

    # --------------------------------
    # Build context for LLM
    # --------------------------------

    messages = build_context(
        summary=summary,
        conversation=conversation,
        recent_count=10
    )

    assistant_response = ""

    input_tokens = 0
    output_tokens = 0
    total_tokens = 0
    reasoning_tokens = 0

    try:

        with httpx.stream(
            "POST",
            url,
            headers=headers,
            json={
                "model": "openai/gpt-oss-20b",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 200,
                "stream": True,
                "stream_options": {
                    "include_usage": True
                }
            },
            timeout=30,
        ) as response:

            response.raise_for_status()

            print("AI : ", end="", flush=True)

            for line in response.iter_lines():

                if not line:
                    continue

                if not line.startswith("data: "):
                    continue

                data = line[6:]

                if data == "[DONE]":
                    break

                chunk = json.loads(data)

                # -----------------------------
                # Assistant content
                # -----------------------------

                choices = chunk.get("choices", [])

                if choices:

                    delta = choices[0].get(
                        "delta",
                        {}
                    )

                    content = delta.get("content")

                    if content:

                        print(
                            content,
                            end="",
                            flush=True
                        )

                        assistant_response += content

                # -----------------------------
                # Usage
                # -----------------------------

                usage = chunk.get("usage")

                if usage:

                    input_tokens = usage.get(
                        "prompt_tokens",
                        0
                    )

                    output_tokens = usage.get(
                        "completion_tokens",
                        0
                    )

                    total_tokens = usage.get(
                        "total_tokens",
                        0
                    )

                    details = (
                        usage.get(
                            "completion_tokens_details"
                        ) or {}
                    )

                    reasoning_tokens = details.get(
                        "reasoning_tokens",
                        0
                    )

        print()

        # --------------------------------
        # Save full response
        # --------------------------------

        conversation.append({
            "role": "assistant",
            "content": assistant_response
        })

        # --------------------------------
        # Cost
        # --------------------------------

        turn_cost = calculate_cost(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        total_cost += turn_cost

        print()
        print("Input tokens     :", input_tokens)
        print("Output tokens    :", output_tokens)
        print("Total tokens     :", total_tokens)
        print("Reasoning tokens :", reasoning_tokens)
        print(f"Turn cost        : ${turn_cost:.8f}")
        print(f"Total cost       : ${total_cost:.8f}")
        print()

    except httpx.HTTPError as e:

        print(f"\nAPI error: {e}")