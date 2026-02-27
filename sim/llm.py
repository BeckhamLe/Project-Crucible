"""Thin LLM API wrapper. Swap models by changing MODEL."""

import os
import time
import anthropic

MODEL = "claude-haiku-4-5-20251001"

_client = None

MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # seconds


def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def call_llm(system_prompt: str, user_prompt: str, model: str = None) -> dict:
    """Call the LLM and return {"text": ..., "input_tokens": ..., "output_tokens": ...}."""
    client = get_client()
    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=model or MODEL,
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return {
                "text": response.content[0].text,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        except anthropic.APIStatusError as e:
            if e.status_code in (429, 529) and attempt < MAX_RETRIES - 1:
                wait = INITIAL_BACKOFF * (2 ** attempt)
                print(f"  [retry {attempt+1}/{MAX_RETRIES}] API {e.status_code}, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
