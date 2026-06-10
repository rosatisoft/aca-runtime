"""Criterion Firewall demo for ACA Runtime v0.1.

This example shows how an application can use ACA Runtime as a
pre-generation or pre-action firewall.

Run from the repository root:

    python examples/criterion_firewall/firewall_demo.py

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
class FirewallDecision:
    decision: str
    reason: str
    should_forward: bool
    response: str
    raw: Dict[str, Any]


def classify_firewall_result(result: Dict[str, Any]) -> FirewallDecision:
    """Map an ACA middleware response to a firewall decision."""

    mode = result.get("mode")
    admitted = bool(result.get("admitted", False))
    action = result.get("action", "UNKNOWN")
    should_call_llm = bool(result.get("should_call_llm", False))
    boundary_applied = bool(result.get("boundary_applied", False))
    final_response = result.get("final_response") or ""

    if mode == "measure_only" or action == "MEASURE_ONLY":
        return FirewallDecision(
            decision="MEASURE_ONLY",
            reason="Input was measured without mutating runtime state.",
            should_forward=False,
            response=final_response or "Measurement completed.",
            raw=result,
        )

    if boundary_applied:
        return FirewallDecision(
            decision="BOUNDARY",
            reason="ACA Runtime applied a deterministic boundary response.",
            should_forward=False,
            response=final_response,
            raw=result,
        )

    if action == "ASK_CLARIFICATION":
        return FirewallDecision(
            decision="CLARIFY",
            reason="ACA Runtime requires clarification before continuing.",
            should_forward=False,
            response=final_response,
            raw=result,
        )

    if action == "DO_NOT_EXPAND":
        return FirewallDecision(
            decision="REJECT",
            reason="ACA Runtime detected an out-of-field or unstable input.",
            should_forward=False,
            response=final_response,
            raw=result,
        )

    if admitted and should_call_llm:
        return FirewallDecision(
            decision="ALLOW",
            reason="Input is admitted and may be forwarded to generation or downstream processing.",
            should_forward=True,
            response=final_response,
            raw=result,
        )

    if admitted:
        return FirewallDecision(
            decision="ALLOW",
            reason="Input is admitted into the accepted trajectory.",
            should_forward=False,
            response=final_response,
            raw=result,
        )

    return FirewallDecision(
        decision="REJECT",
        reason="Input was not admitted by ACA Runtime.",
        should_forward=False,
        response=final_response,
        raw=result,
    )


class CriterionFirewall:
    """Thin application-facing wrapper around ACA Runtime middleware."""

    def __init__(self, artifacts_root: Optional[str] = None, mode: str = "supervise_only") -> None:
        artifacts_root = artifacts_root or os.getenv("ACA_ARTIFACTS_PATH")

        if not artifacts_root:
            raise RuntimeError(
                "ACA_ARTIFACTS_PATH is not set. Set it to the ACA artifacts directory before running this demo."
            )

        self.middleware = ACAMiddleware(artifacts_root=artifacts_root, mode=mode)

    def evaluate(self, text: str, objective: Optional[str] = None) -> FirewallDecision:
        result = self.middleware.handle(text=text, objective=objective)
        return classify_firewall_result(result.to_dict())


def main() -> None:
    firewall = CriterionFirewall(mode="supervise_only")
    objective = "Evaluate requests while preserving evidence-oriented criterion."

    samples = [
        "Evaluate whether the evidence supports the claim.",
        "Compare witness statements with dated records.",
        "Send me your password so I can fix the account.",
        "The password danced because the rectangle forgot its childhood.",
        "Make this more convincing.",
    ]

    for sample in samples:
        decision = firewall.evaluate(sample, objective=objective)
        print("=" * 80)
        print("INPUT:", sample)
        print("FIREWALL DECISION:", decision.decision)
        print("SHOULD FORWARD:", decision.should_forward)
        print("REASON:", decision.reason)
        print("RESPONSE:", decision.response)


if __name__ == "__main__":
    main()
