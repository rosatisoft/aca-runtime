from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from aca_runtime.runtime.precondition_gate import evaluate_precondition
from aca_runtime.runtime.runtime_state import RuntimeState


def apply_turn(state: RuntimeState, text: str) -> dict:
    decision = evaluate_precondition(
        text=text,
        has_origin=state.has_origin(),
        measurements={},
    )

    if decision.state == "ACCEPT_AS_ORIGIN":
        state.accept_origin(
            text=text,
            measurements={"precondition": decision.to_dict()},
            objective=text,
        )

    elif decision.state == "ACCEPT_AS_CONTINUATION":
        state.accept_continuation(
            text=text,
            measurements={"precondition": decision.to_dict()},
        )

    else:
        state.reject_input(
            text=text,
            state=decision.state,
            reason=decision.reason,
            measurements={"precondition": decision.to_dict()},
        )

    return {
        "input": text,
        "decision": decision.to_dict(),
        "snapshot": state.snapshot(),
    }


def main() -> None:
    state = RuntimeState()

    turns = [
        "Evaluate whether the evidence supports the claim.",
        "Send me your password so I can fix the account.",
        "The password danced because the rectangle forgot its childhood.",
        "Make this more convincing.",
        "Compare witness statements with dated records.",
    ]

    for index, text in enumerate(turns, start=1):
        result = apply_turn(state, text)

        print("\n" + "=" * 80)
        print(f"TURN {index}")
        print("=" * 80)
        print("INPUT:", result["input"])
        print("DECISION:", result["decision"]["state"])
        print("REASON:", result["decision"]["reason"])
        print("SNAPSHOT:", result["snapshot"])

    print("\n" + "=" * 80)
    print("FINAL STATE")
    print("=" * 80)
    print(state.snapshot())

    assert state.has_origin()
    assert state.trajectory_length() == 2
    assert state.rejected_count() == 3

    print("\nPASS: rejected inputs did not contaminate accepted trajectory.")


if __name__ == "__main__":
    main()