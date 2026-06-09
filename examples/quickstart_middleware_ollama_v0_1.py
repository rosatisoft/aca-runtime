from __future__ import annotations

import json
import os

from aca_runtime.middleware import ACAMiddleware
from aca_runtime.runtime.llm_providers.ollama_provider import OllamaProvider


def main() -> None:
    artifacts_root = os.environ.get("ACA_ARTIFACTS_PATH")

    if not artifacts_root:
        raise RuntimeError(
            "ACA_ARTIFACTS_PATH is not set. "
            "Example: $env:ACA_ARTIFACTS_PATH='C:\\path\\to\\ACA\\artifacts'"
        )

    provider = OllamaProvider(
        model=os.environ.get("ACA_OLLAMA_MODEL", "phi4-mini"),
        host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
    )

    middleware = ACAMiddleware(
        artifacts_root=artifacts_root,
        mode="generate",
        llm_provider=provider,
    )

    result = middleware.handle(
        text="Evaluate whether the evidence supports the claim.",
        objective="Analyze claims using only available evidence.",
    )

    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
