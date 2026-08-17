# 2.1 Model Bake-off

This directory contains a unified framework and benchmark scripts to evaluate and compare multiple LLM providers (e.g., Groq, OpenRouter, Ollama) using a common interface (`ModelInterface`).

---

## 📁 Project Structure

- **`models/base.py`**: Defines abstract base class `ModelInterface` and response data structure `ModelResponse` (latency, tokens, content).
- **`models/groq.py`**: Groq API provider implementation.
- **`models/openrouter.py`**: OpenRouter API provider implementation.
- **`models/ollama.py`**: Ollama local model provider implementation.
- **`app.py`**: OpenRouter direct API invocation with retry logic and exponential backoff for handling rate limits (HTTP 429).
- **`benchmark.py`**: Benchmarking script for comparing response latency, input/output/total token usage across different models.

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- `uv` package manager
- Set required API keys in `.env` at the root directory:
  ```env
  GROQ_API_KEY=gsk_your_groq_api_key
  OPENROUTER_API_KEY=sk-or-v1-your_openrouter_api_key
  ```

### Running the App & Benchmark

```bash
# Run OpenRouter chat client script
uv run python "week-2/2.1 Model bake-off/app.py"

# Run Model Benchmark comparison script
uv run python "week-2/2.1 Model bake-off/benchmark.py"
```
