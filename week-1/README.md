# Week 1: AI Training & LLM Fundamentals

This directory contains the projects, exercises, and code samples for **Week 1** of the AI Training course.

---

## 📁 Directory Structure & Headlines

### 1. `1.1 Talk to a public API`
- **Headline**: **Introduction to HTTP Requests & Public APIs**
- **Description**: Demonstrates how to send HTTP GET requests to public REST APIs (such as Open-Meteo) using `httpx`, handle parameters, and parse JSON responses.

### 2. `1.2 Your first model call`
- **Headline**: **First LLM Integration with Groq API**
- **Description**: A interactive command-line interface (CLI) chat loop that sends user input to Groq's Llama 3.3 model using HTTP POST requests and streams back the completion output.

### 3. `1.3 Token and cost reporting`
- **Headline**: **FastAPI Chat Endpoint with Token Usage Tracking & Summarization**
- **Description**: A FastAPI REST API service featuring automatic conversation truncation, background prompt summarization for context compression, and token usage reporting (`input_token`, `output_tokens`, `total_tokens`).

### 4. `1.4 Temperature and the context window`
- **Headline**: **LLM Hyperparameters, Determinism & Context Limits**
- **Description**: Hands-on experiments exploring LLM parameters:
  - Comparing output determinism at low temperature (`0.0`) vs high temperature (`1.0`).
  - Token truncation handling when setting `max_tokens` too low.
  - Observing API exceptions and limits when exceeding model context windows.

### 5. `statelessFunction`
- **Headline**: **Stateless Architecture Patterns for LLMs**
- **Description**: Core concepts and scripts demonstrating stateless request handling and maintaining state externally across model invocations.

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) package manager installed
- A valid Groq API Key set in `.env` at the root directory:
  ```env
  GROQ_API_KEY=gsk_your_api_key_here
  ```

### Running an Exercise
Navigate to the root directory and run any application script using `uv`:

```bash
# Run 1.1 Public API script
uv run python "week-1/1.1 Talk to a public API/app.py"

# Run 1.2 Interactive model call
uv run python "week-1/1.2 Your first model call/app.py"

# Run 1.4 Temperature & Context Window experiment
uv run python "week-1/1.4 Temperature and the context window/app.py"
```

For FastAPI services (e.g. `1.3 Token and cost reporting`):
```bash
uv run python -m uvicorn "week-1.1.3 Token and cost reporting.app:app" --reload
```
