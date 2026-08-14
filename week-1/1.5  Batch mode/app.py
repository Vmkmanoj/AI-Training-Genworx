import os
import asyncio
import time

import httpx
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

MODEL = "llama-3.3-70b-versatile"
url = os.getenv("url")


headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

INPUT_COST_PER_1M = 0.15
OUTPUT_COST_PER_1M = 0.60

PROMPTS_FILE = os.path.join(os.path.dirname(__file__), "prompts.txt")


# ============================================================
# READ PROMPTS
# ============================================================

def load_prompts(filename: str) -> list[str]:

    with open(filename, "r", encoding="utf-8") as file:

        prompts = [
            line.strip()
            for line in file
            if line.strip()
        ]

    return prompts


# ============================================================
# CALCULATE COST
# ============================================================

def calculate_cost(usage: dict) -> float:

    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_COST_PER_1M

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_COST_PER_1M

    return input_cost + output_cost


# ============================================================
# ONE MODEL CALL
# ============================================================

async def send_prompt(prompt: str, client: httpx.AsyncClient, semaphore: asyncio.Semaphore = None):

    async def _call():
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }

        retries = 8
        backoff = 2.0

        for attempt in range(retries):
            try:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30.0,
                )

                if response.status_code == 429:
                    await asyncio.sleep(backoff)
                    backoff *= 1.5
                    continue

                response.raise_for_status()
                data = response.json()

                answer = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})

                cost = calculate_cost(usage)

                return {
                    "prompt": prompt,
                    "answer": answer,
                    "input_tokens": usage.get("prompt_tokens", 0),
                    "output_tokens": usage.get("completion_tokens", 0),
                    "cost": cost
                }
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 429 and attempt < retries - 1:
                    await asyncio.sleep(backoff)
                    backoff *= 1.5
                    continue
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(backoff)
                backoff *= 1.5

        raise RuntimeError(f"Failed to fetch response for prompt: {prompt}")

    if semaphore:
        async with semaphore:
            return await _call()
    else:
        return await _call()


# ============================================================
# SEQUENTIAL MODE
# ============================================================

async def run_sequential(prompts):

    print("\n" + "=" * 70)
    print("SEQUENTIAL MODE")
    print("=" * 70)

    results = []

    start_time = time.perf_counter()

    async with httpx.AsyncClient() as client:
        for prompt in prompts:

            result = await send_prompt(prompt, client)

            results.append(result)

            print(f"\nPrompt: {prompt}")
            print(f"Cost: ${result['cost']:.8f}")

    elapsed = time.perf_counter() - start_time

    total_cost = sum(
        result["cost"]
        for result in results
    )

    average_cost = total_cost / len(results)

    return {
        "results": results,
        "elapsed": elapsed,
        "total_cost": total_cost,
        "average_cost": average_cost
    }


# ============================================================
# CONCURRENT / BATCH MODE
# ============================================================

async def run_batch(prompts, max_concurrency: int = 2):

    print("\n" + "=" * 70)
    print(f"CONCURRENT / BATCH MODE (Max Concurrency: {max_concurrency})")
    print("=" * 70)

    start_time = time.perf_counter()

    semaphore = asyncio.Semaphore(max_concurrency)

    async with httpx.AsyncClient() as client:
        # Create all requests with concurrency limits
        tasks = [
            send_prompt(prompt, client, semaphore=semaphore)
            for prompt in prompts
        ]

        # Wait for all requests concurrently
        results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start_time

    total_cost = sum(
        result["cost"]
        for result in results
    )

    average_cost = total_cost / len(results)

    for result in results:

        print(f"\nPrompt: {result['prompt']}")

        print(
            f"Input tokens: "
            f"{result['input_tokens']}"
        )

        print(
            f"Output tokens: "
            f"{result['output_tokens']}"
        )

        print(
            f"Cost: "
            f"${result['cost']:.8f}"
        )

        print(
            f"Answer: "
            f"{result['answer'][:100]}..."
        )

    return {
        "results": results,
        "elapsed": elapsed,
        "total_cost": total_cost,
        "average_cost": average_cost
    }


# ============================================================
# MAIN
# ============================================================

async def main():

    prompts = load_prompts(PROMPTS_FILE)

    print(f"\nLoaded {len(prompts)} prompts.")

    if len(prompts) != 20:

        print(
            f"WARNING: Expected 20 prompts, "
            f"but found {len(prompts)}."
        )

    # --------------------------------------------------------
    # Sequential
    # --------------------------------------------------------

    sequential = await run_sequential(prompts)

    # --------------------------------------------------------
    # Concurrent
    # --------------------------------------------------------

    batch = await run_batch(prompts)

    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"\nNumber of prompts: "
        f"{len(prompts)}"
    )

    print(
        f"\nSequential elapsed time: "
        f"{sequential['elapsed']:.2f} seconds"
    )

    print(
        f"Batch elapsed time: "
        f"{batch['elapsed']:.2f} seconds"
    )

    print(
        f"\nSequential total cost: "
        f"${sequential['total_cost']:.8f}"
    )

    print(
        f"Batch total cost: "
        f"${batch['total_cost']:.8f}"
    )

    print(
        f"\nBatch average cost per prompt: "
        f"${batch['average_cost']:.8f}"
    )

    # --------------------------------------------------------
    # SPEEDUP
    # --------------------------------------------------------

    speedup = (
        sequential["elapsed"]
        / batch["elapsed"]
    )

    print(
        f"\nSpeedup: "
        f"{speedup:.2f}x"
    )

    print("\nDone.")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())