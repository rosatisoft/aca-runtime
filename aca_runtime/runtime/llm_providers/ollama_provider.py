from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, Optional

from .base import LLMResponse


class OllamaProvider:
    provider_name = "ollama"

    def __init__(
        self,
        model: str = "phi4-mini",
        host: str = "http://localhost:11434",
    ):
        self.model = model
        self.host = host.rstrip("/")

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        if options:
            payload["options"] = options

        request = urllib.request.Request(
            url=f"{self.host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))

        return LLMResponse(
            provider=self.provider_name,
            model=self.model,
            prompt=prompt,
            response=data.get("response", ""),
            metadata={
                "raw": data,
            },
        )


if __name__ == "__main__":
    provider = OllamaProvider(model="phi4-mini")
    result = provider.generate(
        prompt="Say hello in one sentence.",
        options={
            "temperature": 0.2,
            "num_predict": 80,
        },
    )

    print(result.response)