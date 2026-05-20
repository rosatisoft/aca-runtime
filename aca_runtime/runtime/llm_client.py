import os

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


def call_llm(
    user_message: str,
    system_message: str | None = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = []

    if system_message:
        messages.append({
            "role": "system",
            "content": system_message,
        })

    messages.append({
        "role": "user",
        "content": user_message,
    })

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    content = response.choices[0].message.content

    usage = response.usage

    return {
        "content": content,
        "model": model,
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        },
    }