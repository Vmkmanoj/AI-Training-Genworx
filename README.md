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

### 6. `1.5  Batch mode`
- **Headline**: **Batch & Concurrent LLM Processing with Concurrency Control**
- **Description**: Demonstrates processing multiple prompts asynchronously using `asyncio` and `httpx`. Compares sequential processing vs concurrent batch execution using `asyncio.Semaphore`, featuring rate limiting, automatic backoff retries (handling HTTP 429), and speedup/cost comparison metrics.

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

# Run 1.5 Batch mode experiment
uv run python "week-1/1.5  Batch mode/app.py"
```

For FastAPI services (e.g. `1.3 Token and cost reporting`):
```bash
uv run python -m uvicorn "week-1.1.3 Token and cost reporting.app:app" --reload
```

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

## 📊 Benchmark Results Comparison

Prompt tested: *"What is the capital of France?"*

### 1. `OpenRouterModel` (`nvidia/nemotron-nano-9b-v2:free`)
```text
Answer: 

The capital of France is **Paris**.

Input tokens: 19
Output tokens: 159
Total tokens: 178
Latency: 19.77s
```

### 2. `OpenRouterModel` (`openai/gpt-oss-20b:free`)
```text
Answer: The capital of France is **Paris**.
Input tokens: 74
Output tokens: 40
Total tokens: 114
Latency: 2.22s
```

### 3. `GroqModel` (`openai/gpt-oss-20b`)
```text
Answer: The capital of France is **Paris**.
Input tokens: 78
Output tokens: 40
Total tokens: 118
Latency: 0.54s
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.12+
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

### 2.2 A real conversation

The directory contains a framework to run a real conversation with a Groq model.

- Context_window: 8192 tokens
- Summarization for every 10 turns
- max-token : 200
- temperature : 0.5


(.venv) PS C:\workspace\AI-Training-Genworx\week-2\2.2 A real conversation> python app.py
You : hai
AI : Hello! How can I help you today?

Input tokens     : 81
Output tokens    : 32
Total tokens     : 113
Reasoning tokens : 14
Turn cost        : $0.00001568
Total cost       : $0.00001568

You : how are you my name is manojkumar
AI : Hello Manojkumar! I’m just a bunch of code, so I don’t have feelings in the way humans do, but I’m here and ready to help you. How can I assist you today?

Input tokens     : 110
Output tokens    : 64
Total tokens     : 174
Reasoning tokens : 13
Turn cost        : $0.00002745
Total cost       : $0.00004313

You : so how can you helpfull for me
AI : I’m here to make your life a little easier—whether that means answering questions, brainstorming ideas, or just having a quick chat. Here are some of the things I can help you with:

| What you need | How I can help |
|---------------|----------------|
| **Information & research** | Quick facts, explanations, and deeper dives on topics like science, history, tech, health, and more. |
| **Writing & editing** | Draft emails, reports, essays, blog posts, or creative stories; polish grammar, style, and tone. |
| **Learning & tutoring** | Step‑by‑step explanations, practice problems, or study guides for subjects like math, coding, languages, etc. |
| **Planning & organization** | Create schedules, to‑do lists, project plans, or event itineraries. |
| **Coding & debugging** | Write snippets

Input tokens     : 170
Output tokens    : 200
Total tokens     : 370
Reasoning tokens : 13
Turn cost        : $0.00007275
Total cost       : $0.00011588

You : so what is my name
AI : You mentioned earlier that your name is **Manojkumar**. If that’s correct, I’ll keep that in mind for our conversation. If you’d prefer a different nickname or have anything else to share, just let me know!

Input tokens     : 364
Output tokens    : 102
Total tokens     : 466
Reasoning tokens : 44
Turn cost        : $0.00005790
Total cost       : $0.00017378

You : okey then , let work on project called chatbot
AI : Great! Let’s build a chatbot together. 🚀

To get started, I just need a bit more context so I can tailor the guidance to your exact needs:

| What I’d like to know | Why it matters |
|-----------------------|----------------|
| **Purpose** – What will the chatbot do? (e.g., customer support, personal assistant, FAQ bot, etc.) | Determines the required knowledge base, flow, and integrations. |
| **Platform** – Where will it live? (Web, mobile, Slack, Discord, Telegram, WhatsApp, etc.) | Influences the SDKs, APIs

Input tokens     : 433
Output tokens    : 200
Total tokens     : 633
Reasoning tokens : 67
Turn cost        : $0.00009247
Total cost       : $0.00026625

You : her let try new technial drive
AI : 

Input tokens     : 613
Output tokens    : 200
Total tokens     : 813
Reasoning tokens : 198
Turn cost        : $0.00010598
Total cost       : $0.00037223

You : what is my name
AI : Your name is **Manojkumar**.

Input tokens     : 607
Output tokens    : 51
Total tokens     : 658
Reasoning tokens : 32
Turn cost        : $0.00006083
Total cost       : $0.00043305

You : what i am going to work with you
AI : You’re going to work with me on building a chatbot—think of it as a collaborative coding and design session. Here’s what that looks like:

| Step | What we’ll do together | Your role |
|------|------------------------|-----------|
| **1️⃣ Define the goal** | We decide what the bot should do (customer support, FAQ, personal assistant, e etc.). | Share your vision and any specific requirements. |
| **2️⃣ Choose a platform** | Pick where the bot will live (web, mobile, Slack, Discord, etc.). | Let me k know the target environment(s). |
| **3️⃣ Pick a tech stack** | Select

Input tokens     : 568
Output tokens    : 200
Total tokens     : 768
Reasoning tokens : 58
Turn cost        : $0.00010260
Total cost       : $0.00053565

You : okey can we work on it ?
AI : Absolutely! 🎉 Let’s kick things off by laying out a simple, step‑by‑step roadmap. Once we nail down a few key decisions, I’ll walk you through the code, the architecture, and the deployment process—everything you need to get a working chatbot up and running.

---

## 1️⃣ Clarify the Goal
**What should the bot do?**  
- Customer support (FAQ, ticketing, live chat)
- Personal assistant (calendar, reminders, info lookup)  
- Knowledge base / FAQ bot  
- Entertainment (games, trivia)  
- Anything else?

> *Why it matters:* The bot’s purpose determines the data sources, conversation flow, and required

Input tokens     : 575
Output tokens    : 200
Total tokens     : 775
Reasoning tokens : 49
Turn cost        : $0.00010312
Total cost       : $0.00063878

You : my mentor said you have to focus on ai becose ai is now very inportn now days
AI : Sure thing!  
Let’s build an **AI‑powered chatbot** that feels smart, learns from conversation, and can be deployed wherever you need it. Below is a practical, step‑by‑step playbook that covers everything from the high‑level idea to the final code you’ll run.

---

## 1️⃣ Decide the *Type* of AI Chatbot

| Option | What it’s good for | Typical tech |
|--------|--------------------|--------------|
| **Retrieval‑Augmented** (e.g., RAG) | Pulls facts from a knowledge base or the web | LangChain + LlamaIndex + OpenAI/Claude |
| **Generative** (LLM‑only) | Free‑form conversation, creative answers | OpenAI GPT

Input tokens     : 711
Output tokens    : 200
Total tokens     : 911
Reasoning tokens : 35
Turn cost        : $0.00011333
Total cost       : $0.00075210

You : what my mentor said
AI : Your mentor’s point is spot‑on: **AI is the “must‑have” technology for any modern chatbot**.  
Here’s a quick recap of what they’re encouraging you to do, and why it matters:

| Why AI matters | What it unlocks for your bot | How we’ll get it done |
|----------------|-----------------------------|-----------------------|
| **Context‑aware responses** | The bot can understand user intent and produce natural language replies, instead of rigid keyword‑based rules. | Use a large language model (LLM) such as OpenAI’s GPT‑4, Anthropic Claude, or

Input tokens     : 794
Output tokens    : 200
Total tokens     : 994
Reasoning tokens : 66
Turn cost        : $0.00011955
Total cost       : $0.00087165

You : what is ai
AI : **AI** – *Artificial Intelligence* – is a branch of computer science that builds systems capable of performing tasks that normally require human intelligence. These tasks include:

| Task | Typical AI Technique | Example |
|------|----------------------|---------|
| **Understanding language** | Natural Language Processing (NLP) | Chatbots, sentiment analysis |
| **Generating language** | Language Models (LLMs) | GPT‑4, Claude, Llama |
| **Seeing images** | Computer Vision | Object detection, image captioning |
| **Making decisions** | Reinforcement Learning, Decision Trees | Game‑playing agents, recommendation engines |
| **Learning from data** | Machine Learning, Deep Learning | Predictive models, fraud detection |

In a chatbot context, AI mainly means using an LLM to interpret what a user says and to produce a human‑like reply. The model

Input tokens     : 867
Output tokens    : 200
Total tokens     : 1067
Reasoning tokens : 15
Turn cost        : $0.00012502
Total cost       : $0.00099668

You : what is react
AI : ### What is React?

**React** (often called *React.js* or *ReactJS*) is an open‑source JavaScript library created by Facebook for building user interfaces—especially single‑page web applications. It lets you describe the UI in **components**, which are reusable, self‑contained pieces of code that render a part of the screen.

---

#### Key Concepts

| Concept | What it is | Why it matters |
|---------|------------|----------------|
| **Component** | A JavaScript function or class that returns JSX (HTML‑like syntax). | Reusability & isolation of UI logic. |
| **JSX** | A syntax extension that lets you write HTML inside JavaScript. | Makes UI code

Input tokens     : 1028
Output tokens    : 200
Total tokens     : 1228
Reasoning tokens : 45
Turn cost        : $0.00013710
Total cost       : $0.00113378

You : what is python
AI : **Python** is a high‑level, general‑purpose programming language that emphasizes readability, simplicity, and rapid development. Created by Guido van Rossum and first released in 1991, Python is now one of the most popular languages in the world.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Readable syntax** | Uses indentation to define code blocks instead of braces or keywords. |
| **Interpreted** | Runs line‑by‑line, which speeds up development and debugging. |
| **Dynamic typing** | Variables don’t need explicit type declarations. |
| **Extensive standard library** | “Batteries included” – modules for file I/O, networking, web services, data manipulation, and more. |
| **Cross‑platform** | Works on Windows, macOS, Linux, and many other operating systems. |
| **Large

Input tokens     : 1155
Output tokens    : 200
Total tokens     : 1355
Reasoning tokens : 12
Turn cost        : $0.00014662
Total cost       : $0.00128040

You : what is java
AI : ### What is Java?

**Java** is a high‑level, object‑oriented programming language and runtime environment designed by James Gosling and the team at Sun Microsystems (now Oracle) and first released in 1995. It’s widely used for building enterprise applications, Android apps, web services, and more.

---

#### Core Principles

| Principle | What it means |
|-----------|---------------|
| **Write Once, Run Anywhere (WORA)** | Java code compiles to bytecode that runs on the Java Virtual Machine (JVM), which is available on virtually every platform. |
| **Object‑Oriented (OO)** | Everything is an object (or a class); encourages encapsulation, inheritance, and polymorphism. |
| **Strongly Typed** | Types are checked at compile time, reducing runtime errors. |
| **Garbage‑Collected** | Automatic memory management frees

Input tokens     : 1056
Output tokens    : 200
Total tokens     : 1256
Reasoning tokens : 11
Turn cost        : $0.00013920
Total cost       : $0.00141960

You : what kotalin
AI : **Kotlin** is a modern, statically‑typed programming language that runs on the Java Virtual Machine (JVM) and can also be compiled to JavaScript or native binaries (via Kotlin/Native). It was created by JetBrains and first released in 2011. In 2017 Google announced Kotlin as an officially supported language for Android development, and today it’s widely used for Android, backend services, desktop applications, and even web front‑ends.

---

## 1. Why Kotlin?  What Makes It Special?

| Feature | What It Gives You | Why It Matters |
|---------|------------------|----------------|
| **Concise syntax** | Less boilerplate (no

| **Strongly Typed** | Types are checked at compile time, reducing runtime errors. |
| **Garbage‑Collected** | Automatic memory management frees

Input tokens     : 1056
Output tokens    : 200
Total tokens     : 1256
Reasoning tokens : 11
Turn cost        : $0.00013920
Total cost       : $0.00141960

You : what kotalin
AI : **Kotlin** is a modern, statically‑typed programming language that runs on the Java Virtual Machine (JVM) and can also be compiled to JavaScript or native binaries (via Kotlin/Native). It was created by JetBrains and first released in 2011. In 2017 Google announced Kotlin as an officially supported language for Android development, and today it’s widely used for Android, backend services, desktop applications, and even web front‑ends.

---

## 1. Why Kotlin?  What Makes It Special?

| Feature | What It Gives You | Why It Matters |
|---------|------------------|----------------|
| **Concise syntax** | Less boilerplate (no

Turn cost        : $0.00013920
Total cost       : $0.00141960

You : what kotalin
AI : **Kotlin** is a modern, statically‑typed programming language that runs on the Java Virtual Machine (JVM) and can also be compiled to JavaScript or native binaries (via Kotlin/Native). It was created by JetBrains and first released in 2011. In 2017 Google announced Kotlin as an officially supported language for Android development, and today it’s widely used for Android, backend services, desktop applications, and even web front‑ends.

---

## 1. Why Kotlin?  What Makes It Special?

| Feature | What It Gives You | Why It Matters |
|---------|------------------|----------------|
| **Concise syntax** | Less boilerplate (no

## 1. Why Kotlin?  What Makes It Special?

| Feature | What It Gives You | Why It Matters |
|---------|------------------|----------------|
| **Concise syntax** | Less boilerplate (no


Input tokens     : 1204
Output tokens    : 200
Total tokens     : 1404
Reasoning tokens : 52
Turn cost        : $0.00015030
Total cost       : $0.00156990

## 🚀 How to Run

### Prerequisites
- Python 3.12+
- `uv` package manager
- Set required API keys in `.env` at the root directory:
  ```env
  GROQ_API_KEY=gsk_your_groq_api_key
  ```

### Running the App & Benchmark

```bash
# Run OpenRouter chat client script
uv run python "week-2/2.2 A real conversation/app.py"

```