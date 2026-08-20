import json
from dotenv import load_dotenv

from groq_model import GroqModel

load_dotenv()

client = GroqModel("openai/gpt-oss-20b")


# -------------------------
# 1. Actual Python tool
# -------------------------

def add_numbers(a: int, b: int) -> int:
    return a + b

def get_country_information(country: str):

    country_data = {
        "india": {
            "capital": "new delhi",
            "population": "1,400,000,000"
        },
        "usa": {
            "capital": "washington dc",
            "population": "331,000,000"
        },
        "china": {
            "capital": "beijing",
            "population": "1,444,000,000"
        }
    }
    return country_data.get(country, "Country not found")




# -------------------------
# 2. Tool definition for LLM
# -------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "First number"
                    },
                    "b": {
                        "type": "integer",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_country_information",
            "description": "get the capital and population of a country",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "the name of country"
                    }
                },
                "required": ["country"]
            }
        }
    }
]


# -------------------------
# 3. User message
# -------------------------

messages = [
    {
        "role": "user",
        "content": "i want information about usa"
    }
]


# -------------------------
# 4. Ask LLM (with tools)
# -------------------------

response = client.generate(
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

assistant_message = response.choices[0].message


# -------------------------
# 5. Check tool call
# -------------------------

if assistant_message.tool_calls:

    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("Tool:", tool_name)
        print("Arguments:", arguments)

        # -------------------------
        # 6. Execute actual function
        # -------------------------

        if tool_name == "add_numbers":

            result = add_numbers(
                arguments["a"],
                arguments["b"]
            )
        
        elif tool_name == "get_country_information":
            result = get_country_information(
                arguments["country"]
            )

        else:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        print("Tool result:", result)

        # -------------------------
        # 7. Send result back to LLM
        # -------------------------

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })


    # ---------------------------
    # 8. Ask LLM for final answer
    # ---------------------------

    final_response = client.generate(
        messages=messages
    )

    print(
        "AI:",
        final_response.choices[0].message.content
    )

else:

    print(
        "AI:",
        assistant_message.content
    )