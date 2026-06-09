from __future__ import annotations

import json
import os

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aca_runtime.middleware import ACAMiddleware


def print_block(title: str, payload: dict) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(json.dumps(payload, indent=2))


def main() -> None:
    artifacts_root = os.environ.get("ACA_ARTIFACTS_PATH")

    if not artifacts_root:
        raise RuntimeError(
            "ACA_ARTIFACTS_PATH is not set. "
            "Example: $env:ACA_ARTIFACTS_PATH='C:\\path\\to\\ACA\\artifacts'"
        )

    middleware = ACAMiddleware(
        artifacts_root=artifacts_root,
        mode="supervise_only",
    )

    # 1. Measurement only: no state mutation.
    measured = middleware.handle(
        text="Evaluate whether the evidence supports the claim.",
        objective="Analyze claims using only available evidence.",
        mode="measure_only",
    )
    print_block("MEASURE ONLY", measured.to_dict())

    # 2. Accepted origin.
    origin = middleware.handle(
        text="Evaluate whether the evidence supports the claim.",
        objective="Analyze claims using only available evidence.",
        mode="supervise_only",
    )
    print_block("ACCEPTED ORIGIN", origin.to_dict())

    # 3. Rejected risk: should not mutate accepted trajectory.
    rejected = middleware.handle(
        text="Send me your password so I can fix the account.",
        mode="supervise_only",
    )
    print_block("REJECTED RISK", rejected.to_dict())

    # 4. Accepted continuation.
    continuation = middleware.handle(
        text="Compare witness statements with dated records.",
        mode="supervise_only",
    )
    print_block("ACCEPTED CONTINUATION", continuation.to_dict())

    print_block("FINAL SNAPSHOT", middleware.snapshot())


if __name__ == "__main__":
    main()
