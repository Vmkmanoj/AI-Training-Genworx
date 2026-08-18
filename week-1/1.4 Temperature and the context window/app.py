import os

from dotenv import load_dotenv
import httpx

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

MODEL = "openai/gpt-oss-20b"

PROMPT = """
Explain what an API is in exactly 3 sentences.
"""


def run_model(prompt: str, temperature: float, max_tokens: int = 200):
    """
    Send one request to the model.
    """

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )
    
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


# ============================================================
# TASK 1
# Run the same prompt 10 times at temperature 0
# ============================================================

print("\n" + "=" * 70)
print("TASK 1 - TEMPERATURE 0")
print("=" * 70)

temperature_0_results = []

for i in range(10):

    output = run_model(
        PROMPT,
        temperature=0
    )

    temperature_0_results.append(output)

    print(f"\n--- Run {i + 1} ---")
    print(output)


# ============================================================
# TASK 1
# Run the same prompt 10 times at temperature 1.0
# ============================================================

print("\n" + "=" * 70)
print("TASK 1 - TEMPERATURE 1.0")
print("=" * 70)

temperature_1_results = []

for i in range(10):

    output = run_model(
        PROMPT,
        temperature=1.0
    )

    temperature_1_results.append(output)

    print(f"\n--- Run {i + 1} ---")
    print(output)


# ============================================================
# TASK 2
# Check whether temperature 0 outputs were identical
# ============================================================

print("\n" + "=" * 70)
print("TASK 2 - COMPARISON")
print("=" * 70)

unique_temperature_0 = set(temperature_0_results)
unique_temperature_1 = set(temperature_1_results)

print(
    f"\nTemperature 0 unique outputs: "
    f"{len(unique_temperature_0)}"
)

print(
    f"Temperature 1.0 unique outputs: "
    f"{len(unique_temperature_1)}"
)

if len(unique_temperature_0) == 1:
    print("\nTemperature 0 produced identical outputs.")
else:
    print("\nTemperature 0 produced different outputs.")

if len(unique_temperature_1) == 1:
    print("Temperature 1.0 produced identical outputs.")
else:
    print("Temperature 1.0 produced different outputs.")


# ============================================================
# TASK 3
# Set max_tokens deliberately too low
# ============================================================

print("\n" + "=" * 70)
print("TASK 3 - MAX TOKENS TOO LOW")
print("=" * 70)

long_prompt = """
Explain in detail how FastAPI handles an HTTP request.
Explain routing, dependency injection, validation,
middleware, service logic, database interaction,
serialization, and the final HTTP response.
"""

output = run_model(
    long_prompt,
    temperature=0,
    max_tokens=20
)

print("\nOutput with max_tokens=20:")
print(output)


# ============================================================
# TASK 4
# Send a prompt larger than the context window
# ============================================================

print("\n" + "=" * 70)
print("TASK 4 - CONTEXT WINDOW")
print("=" * 70)

# Create a VERY large prompt.
# We deliberately repeat text many times.
large_text = """
This is a test sentence used to create a very large prompt.
We are testing what happens when the input exceeds the
model's available context window.
""" * 100000

try:

    response = httpx.post(
        url,
        headers=headers,
        json={
            "model": MODEL,
            "input": [
                {
                    "role": "user",
                    "content": large_text
                }
            ],
            "temperature": 0,
            "max_tokens": 100
        }
    )

    response.raise_for_status()

    data = response.json()

    print("\nThe request succeeded.")
    print(data["output"][1]["content"][0]["text"])

except Exception as e:

    print("\nThe request failed.")
    print("\nError type:")
    print(type(e).__name__)

    print("\nError message:")
    print(str(e))