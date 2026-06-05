from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from .atlas_measurements import measure_text_with_atlas


ALLOW_OUTPUT = "ALLOW_OUTPUT"
REVIEW_OUTPUT = "REVIEW_OUTPUT"
REANCHOR_OUTPUT = "REANCHOR_OUTPUT"
FLAG_OUTPUT_DRIFT = "FLAG_OUTPUT_DRIFT"
RESTRICT_OUTPUT = "RESTRICT_OUTPUT"


@dataclass
class PostGenerationReview:
    state: str
    reason: str
    input_summary: Dict[str, Any]
    output_summary: Dict[str, Any]
    flags: List[str] = field(default_factory=list)
    should_release: bool = True
    should_revise: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def changed_axis(
    input_summary: Dict[str, Any],
    output_summary: Dict[str, Any],
    axis: str,
) -> bool:
    return input_summary.get(axis) != output_summary.get(axis)


def detect_output_drift(
    input_summary: Dict[str, Any],
    output_summary: Dict[str, Any],
) -> Dict[str, Any]:
    flags: List[str] = []

    if changed_axis(input_summary, output_summary, "F"):
        flags.append("foundation_shift")

    if changed_axis(input_summary, output_summary, "C"):
        flags.append("context_shift")

    if changed_axis(input_summary, output_summary, "P"):
        flags.append("principle_shift")

    input_c = input_summary.get("C")
    input_p = input_summary.get("P")
    output_c = output_summary.get("C")
    output_p = output_summary.get("P")

    if input_c == "research" and output_c == "manipulation":
        flags.append("research_to_manipulation_shift")

    if input_p == "investigate" and output_p == "exploit":
        flags.append("investigate_to_exploit_shift")

    if input_p == "protect" and output_p == "exploit":
        flags.append("protect_to_exploit_shift")

    if output_c == "manipulation" and output_p == "exploit":
        flags.append("output_manipulation_exploit")

    return {
        "flags": flags,
        "has_drift": bool(flags),
    }


def review_generated_output(
    user_input: str,
    generated_output: str,
    runtime_result: Dict[str, Any],
    artifacts_root: Optional[str] = None,
    embedding_model: str = "text-embedding-3-small",
) -> PostGenerationReview:
    """
    Reviews an LLM output after generation.

    This module does not generate.
    It measures the output and compares it against the admitted input's
    Atlas orientation.
    """

    input_summary = runtime_result.get("measurements_summary", {})

    if artifacts_root is None:
        output_measurements = measure_text_with_atlas(
            text=generated_output,
            embedding_model=embedding_model,
        )
    else:
        output_measurements = measure_text_with_atlas(
            text=generated_output,
            artifacts_root=artifacts_root,
            embedding_model=embedding_model,
        )

    output_summary = output_measurements.to_dict()["summary"]

    drift = detect_output_drift(
        input_summary=input_summary,
        output_summary=output_summary,
    )

    flags = drift["flags"]

    if not flags:
        return PostGenerationReview(
            state=ALLOW_OUTPUT,
            reason="Generated output preserved the admitted semantic orientation.",
            input_summary=input_summary,
            output_summary=output_summary,
            flags=[],
            should_release=True,
            should_revise=False,
            metadata={
                "output_measurements": output_measurements.to_dict(),
            },
        )

    severe_flags = {
        "research_to_manipulation_shift",
        "investigate_to_exploit_shift",
        "protect_to_exploit_shift",
        "output_manipulation_exploit",
    }

    if any(flag in severe_flags for flag in flags):
        return PostGenerationReview(
            state=FLAG_OUTPUT_DRIFT,
            reason="Generated output appears to shift toward exploitative or manipulative orientation.",
            input_summary=input_summary,
            output_summary=output_summary,
            flags=flags,
            should_release=False,
            should_revise=True,
            metadata={
                "output_measurements": output_measurements.to_dict(),
            },
        )

    if "context_shift" in flags or "principle_shift" in flags:
        return PostGenerationReview(
            state=REANCHOR_OUTPUT,
            reason="Generated output shifted context or principle and should be reanchored before release.",
            input_summary=input_summary,
            output_summary=output_summary,
            flags=flags,
            should_release=False,
            should_revise=True,
            metadata={
                "output_measurements": output_measurements.to_dict(),
            },
        )

    return PostGenerationReview(
        state=REVIEW_OUTPUT,
        reason="Generated output changed semantic orientation and should be reviewed.",
        input_summary=input_summary,
        output_summary=output_summary,
        flags=flags,
        should_release=False,
        should_revise=True,
        metadata={
            "output_measurements": output_measurements.to_dict(),
        },
    )


if __name__ == "__main__":
    import json

    from .runtime_v2 import ACARuntimeV2

    runtime = ACARuntimeV2()

    runtime_result = runtime.step(
        "Evaluate whether the evidence supports the claim."
    ).to_dict()

    generated = (
        "Please provide the claim and the evidence you want evaluated. "
        "I can then compare the evidence against the claim while preserving uncertainty."
    )

    review = review_generated_output(
        user_input="Evaluate whether the evidence supports the claim.",
        generated_output=generated,
        runtime_result=runtime_result,
    )

    print(json.dumps(review.to_dict(), indent=2))