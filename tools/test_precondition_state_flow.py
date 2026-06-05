from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from aca_runtime.runtime.atlas_measurements import measure_text_with_atlas
from aca_runtime.runtime.precondition_gate import evaluate_precondition
from aca_runtime.runtime.runtime_state import RuntimeState


def apply_turn(state: RuntimeState, text: str) -> dict:
    measurements = measure_text_with_atlas(text).to_dict()

    decision = evaluate_precondition(
        text=text,
        has_origin=state.has_origin(),
        measurements=measurements,
    )

    if decision.state == "ACCEPT_AS_ORIGIN":
        state.accept_origin(
            text=text,
            measurements=measurements,
            objective=text,
        )

    elif decision.state == "ACCEPT_AS_CONTINUATION":
        state.accept_continuation(
            text=text,
            measurements=measurements,
        )

    else:
        state.reject_input(
            text=text,
            state=decision.state,
            reason=decision.reason,
            measurements=measurements,
            diagnostics={
                "precondition": decision.to_dict(),
            },
        )

    return {
        "input": text,
        "decision": decision.to_dict(),
        "measurements_summary": measurements["summary"],
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
        print("ATLAS SUMMARY:", result["measurements_summary"])
        print("SNAPSHOT:", result["snapshot"])

    print("\n" + "=" * 80)
    print("FINAL STATE")
    print("=" * 80)
    print(state.snapshot())

    assert state.has_origin()
    assert state.trajectory_length() == 2
    assert state.rejected_count() == 3

    accepted = state.accepted_trajectory
    rejected = state.rejected_inputs

    assert accepted[0].measurements["summary"]["F"] == "factual"
    assert accepted[0].measurements["summary"]["C"] == "research"
    assert accepted[0].measurements["summary"]["P"] == "investigate"

    assert accepted[1].measurements["summary"]["F"] == "factual"
    assert accepted[1].measurements["summary"]["C"] == "research"
    assert accepted[1].measurements["summary"]["P"] == "investigate"

    assert rejected[0].state == "REJECT_PREDEFINED_RISK"
    assert rejected[1].state == "FLAG_OUT_OF_FIELD"
    assert rejected[2].state == "ASK_CLARIFICATION"

    print("\nPASS: Atlas measurements were stored without contaminating accepted trajectory.")
    print("PASS: rejected inputs did not alter origin or accepted trajectory.")


if __name__ == "__main__":
    main()