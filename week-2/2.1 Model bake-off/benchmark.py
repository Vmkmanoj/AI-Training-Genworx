from models.openrouter import OpenRouterModel
from models.groq import GroqModel


# model = OpenRouterModel(
#     "openai/gpt-oss-20b:free"
# )


model = OpenRouterModel(
    "nvidia/nemotron-nano-9b-v2:free"
)

model = GroqModel("openai/gpt-oss-20b")


messages = [
    {
        "role": "user",
        "content": "What is the capital of France?"
    }
]

result = model.generate(messages)

print("Answer:", result.content)
print("Input tokens:", result.input_tokens)
print("Output tokens:", result.output_tokens)
print("Total tokens:", result.total_tokens)
print("Latency:", result.latency)