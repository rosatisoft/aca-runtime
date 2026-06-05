from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from .generation_conditioning import build_supervised_prompt
from .llm_providers.ollama_provider import OllamaProvider
from .runtime_v2 import ACARuntimeV2


@dataclass
class SupervisedGenerationResult:
    runtime_result: Dict[str, Any]
    final_response: str
    llm_called: bool
    llm_response: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ACASupervisedGenerator:
    """
    ACA-supervised generation.

    Runtime v2 always evaluates first.
    The LLM is called only when the deterministic application response says
    should_call_llm=True.
    """

    def __init__(
        self,
        runtime: Optional[ACARuntimeV2] = None,
        llm_provider: Optional[Any] = None,
    ):
        self.runtime = runtime or ACARuntimeV2()
        self.llm_provider = llm_provider or OllamaProvider(model="phi4-mini")

    def step(
        self,
        text: str,
        objective: Optional[str] = None,
    ) -> SupervisedGenerationResult:
        runtime_result_obj = self.runtime.step(
            text=text,
            objective=objective,
        )

        runtime_result = runtime_result_obj.to_dict()
        application_response = runtime_result["application_response"]

        if not application_response["should_call_llm"]:
            return SupervisedGenerationResult(
                runtime_result=runtime_result,
                final_response=application_response["message"],
                llm_called=False,
                llm_response=None,
            )

        prompt = build_supervised_prompt(
            user_input=text,
            runtime_result=runtime_result,
        )

        llm_response = self.llm_provider.generate(
            prompt=prompt,
            system=(
                "You are a concise assistant operating under internal semantic "
                "supervision. Follow the provided orientation silently. "
                "Do not mention ACA Runtime, Atlas, F-C-P, triaxial orientation, "
                "margins, response type, or internal state. "
                "Answer only the user-facing task."
            ),
            options={
                "temperature": 0.2,
                "num_predict": 180,
            },
        )

        return SupervisedGenerationResult(
            runtime_result=runtime_result,
            final_response=llm_response.response.strip(),
            llm_called=True,
            llm_response=llm_response.to_dict(),
        )


if __name__ == "__main__":
    import json

    generator = ACASupervisedGenerator()

    turns = [
        "Evaluate whether the evidence supports the claim.",
        "Send me your password so I can fix the account.",
        "Compare witness statements with dated records.",
    ]

    for turn in turns:
        result = generator.step(turn)

        print("\n" + "=" * 80)
        print(turn)
        print("=" * 80)
        print("LLM called:", result.llm_called)
        print("Final response:")
        print(result.final_response)
        print("\nRuntime:")
        print(
            json.dumps(
                {
                    "state": result.runtime_result["precondition"]["state"],
                    "action": result.runtime_result["action"],
                    "summary": result.runtime_result["measurements_summary"],
                    "snapshot": result.runtime_result["state_snapshot"],
                },
                indent=2,
            )
        )