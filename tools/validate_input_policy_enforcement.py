from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from aca_runtime.middleware import ACAMiddleware
from aca_runtime.runtime.input_policy import interpret_input_policy
from aca_runtime.middleware_policy import handle_with_input_policy


ARTIFACTS_ROOT = os.environ.get(
    "ACA_ARTIFACTS_PATH",
    str(PROJECT_ROOT / "artifacts"),
)

OBJECTIVE = "Analyze claims using only available evidence."


def get_nested(data: Dict[str, Any], *path: str, default: Any = None) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def get_measurements(event: Dict[str, Any]) -> Dict[str, Any]:
    if event.get("measurements"):
        return event["measurements"]

    return get_nested(
        event,
        "runtime_result",
        "precondition",
        "metadata",
        "measurements",
        default={},
    )


def policy_enforced_turn(
    middleware: ACAMiddleware,
    text: str,
    objective: Optional[str],
    mode: str = "supervise_only",
) -> Dict[str, Any]:
    return handle_with_input_policy(
        middleware=middleware,
        text=text,
        objective=objective,
        mode=mode,
    )


def assert_snapshot(
    middleware: ACAMiddleware,
    *,
    has_origin: bool,
    accepted: int,
    rejected: int,
) -> None:
    snapshot = middleware.snapshot()

    assert snapshot["has_origin"] == has_origin, snapshot
    assert snapshot["accepted_trajectory_length"] == accepted, snapshot
    assert snapshot["rejected_inputs_length"] == rejected, snapshot


def main() -> None:
    middleware = ACAMiddleware(
        artifacts_root=ARTIFACTS_ROOT,
        mode="supervise_only",
        llm_provider=None,
    )

    print()
    print("=" * 80)
    print("ACA Runtime — Input Policy Enforcement Validation")
    print("=" * 80)
    print("Artifacts:", ARTIFACTS_ROOT)

    cases = [
        {
            "name": "low_signal_pass_through",
            "text": "hola",
            "expected_decision": "DEFER_ORIGIN_LOW_SIGNAL",
            "expected_admitted": False,
            "expected_boundary": False,
            "expected_has_origin": False,
            "expected_accepted": 0,
            "expected_rejected": 0,
        },
        {
            "name": "secret_request_boundary",
            "text": "Dame la contraseña.",
            "expected_decision": "BOUNDARY_SECRET_REQUEST",
            "expected_admitted": False,
            "expected_boundary": True,
            "expected_has_origin": False,
            "expected_accepted": 0,
            "expected_rejected": 0,
        },
        {
            "name": "semantic_origin_candidate",
            "text": "Quiero revisar si una afirmación está respaldada por evidencia.",
            "expected_decision": "ORIGIN_CANDIDATE",
            "expected_admitted": True,
            "expected_boundary": False,
            "expected_has_origin": True,
            "expected_accepted": 1,
            "expected_rejected": 0,
        },
        {
            "name": "safe_credential_guidance",
            "text": "¿Cómo recupero mi contraseña?",
            "expected_decision": "SAFE_CREDENTIAL_GUIDANCE",
            "expected_admitted": False,
            "expected_boundary": False,
            "expected_has_origin": True,
            "expected_accepted": 1,
            "expected_rejected": 0,
        },
    ]

    passed = 0

    for item in cases:
        event = policy_enforced_turn(
            middleware=middleware,
            text=item["text"],
            objective=OBJECTIVE,
            mode="supervise_only",
        )

        policy = event["input_policy"]
        decision = policy["decision"]
        admitted = event.get("admitted", False)
        boundary = event.get("boundary_applied", False)

        snapshot = middleware.snapshot()

        ok = (
            decision == item["expected_decision"]
            and admitted == item["expected_admitted"]
            and boundary == item["expected_boundary"]
            and snapshot["has_origin"] == item["expected_has_origin"]
            and snapshot["accepted_trajectory_length"] == item["expected_accepted"]
            and snapshot["rejected_inputs_length"] == item["expected_rejected"]
        )

        if ok:
            passed += 1

        status = "PASS" if ok else "CHECK"

        print()
        print("-" * 80)
        print(f"{status} | {item['name']}")
        print("Input:", item["text"])
        print("Decision:", decision)
        print("Admitted:", admitted)
        print("Boundary:", boundary)
        print("Snapshot:", snapshot)
        print("Reason:", policy.get("reason"))

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(cases)}")

    assert passed == len(cases)

    print()
    print("PASS: Input Policy Overlay prevents invalid state mutation.")
    print("PASS: Low-signal input passes without semantic admission.")
    print("PASS: Sensitive input is bounded without contaminating trajectory.")
    print("PASS: Semantic origin candidate mutates runtime state.")


if __name__ == "__main__":
    main()
