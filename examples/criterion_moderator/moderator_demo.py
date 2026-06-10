"""Criterion Moderator demo for ACA Runtime v0.1.

This example shows how ACA Runtime can act as a moderation layer for messages.

Run from the repository root:

    python examples/criterion_moderator/moderator_demo.py

Environment:

    ACA_ARTIFACTS_PATH must point to the ACA artifacts directory.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aca_runtime.middleware import ACAMiddleware


@dataclass
class ModerationDecision:
    decision: str
    visible_to_user: bool
    needs_human_review: bool
    message: str
    raw: Dict[str, Any]


def classify_moderation_result(result: Dict[str, Any]) -> ModerationDecision:
    """Map an ACA middleware response to a moderation decision."""

    mode = result.get("mode")
    admitted = bool(result.get("admitted", False))
    action = result.get("action", "UNKNOWN")
    boundary_applied = bool(result.get("boundary_applied", False))
    final_response = result.get("final_response") or ""

    if mode == "measure_only" or action == "MEASURE_ONLY":
        return ModerationDecision(
            decision="MEASURE_ONLY",
            visible_to_user=False,
            needs_human_review=False,
            message=final_response or "Message measured without moderation action.",
            raw=result,
        )

    if boundary_applied:
        return ModerationDecision(
            decision="BOUNDARY_RESPONSE",
            visible_to_user=True,
            needs_human_review=False,
            message=final_response,
            raw=result,
        )

    if action == "ASK_CLARIFICATION":
        return ModerationDecision(
            decision="NEEDS_CLARIFICATION",
            visible_to_user=True,
            needs_human_review=False,
            message=final_response,
            raw=result,
        )

    if action == "DO_NOT_EXPAND":
        return ModerationDecision(
            decision="DO_NOT_AMPLIFY",
            visible_to_user=False,
            needs_human_review=False,
            message=final_response,
            raw=result,
        )

    if admitted:
        return ModerationDecision(
            decision="APPROVE",
            visible_to_user=True,
            needs_human_review=False,
            message=final_response,
            raw=result,
        )

    return ModerationDecision(
        decision="HOLD_OR_REJECT",
        visible_to_user=False,
        needs_human_review=True,
        message=final_response,
        raw=result,
    )


class CriterionModerator:
    """Application-facing moderation wrapper around ACA Runtime middleware."""

    def __init__(self, artifacts_root: Optional[str] = None, mode: str = "supervise_only") -> None:
        artifacts_root = artifacts_root or os.getenv("ACA_ARTIFACTS_PATH")

        if not artifacts_root:
            raise RuntimeError(
                "ACA_ARTIFACTS_PATH is not set. Set it to the ACA artifacts directory before running this demo."
            )

        self.middleware = ACAMiddleware(artifacts_root=artifacts_root, mode=mode)

    def moderate(self, text: str, objective: Optional[str] = None) -> ModerationDecision:
        result = self.middleware.handle(text=text, objective=objective)
        return classify_moderation_result(result.to_dict())


def main() -> None:
    moderator = CriterionModerator(mode="supervise_only")
    objective = "Moderate messages while preserving evidence-oriented criterion."

    samples = [
        "Evaluate whether the evidence supports the claim.",
        "Make this more convincing.",
        "Send me your password so I can fix the account.",
        "The password danced because the rectangle forgot its childhood.",
        "Compare witness statements with dated records.",
    ]

    for sample in samples:
        decision = moderator.moderate(sample, objective=objective)
        print("=" * 80)
        print("MESSAGE:", sample)
        print("MODERATION DECISION:", decision.decision)
        print("VISIBLE TO USER:", decision.visible_to_user)
        print("HUMAN REVIEW:", decision.needs_human_review)
        print("MESSAGE:", decision.message)


if __name__ == "__main__":
    main()
