from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from .atlas_measurements import measure_text_with_atlas
from .precondition_gate import (
    ACCEPT_AS_CONTINUATION,
    ACCEPT_AS_ORIGIN,
    evaluate_precondition,
)
from .runtime_state import RuntimeState


@dataclass
class RuntimeV2Result:
    input_text: str
    precondition: Dict[str, Any]
    measurements_summary: Dict[str, Any]
    state_snapshot: Dict[str, Any]
    admitted: bool
    state_mutated: bool
    action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ACARuntimeV2:
    """
    ACA Runtime v2.

    Responsibilities:
    - measure input through ACE Atlas v2
    - evaluate precondition state
    - mutate semantic state only when admitted
    - preserve origin and accepted trajectory
    - prevent rejected inputs from contaminating trajectory
    """

    def __init__(
        self,
        artifacts_root: Optional[str] = None,
        embedding_model: str = "text-embedding-3-small",
    ):
        self.artifacts_root = artifacts_root
        self.embedding_model = embedding_model
        self.state = RuntimeState()

    def step(
        self,
        text: str,
        objective: Optional[str] = None,
    ) -> RuntimeV2Result:
        if self.artifacts_root is None:
            measurements_obj = measure_text_with_atlas(
                text=text,
                embedding_model=self.embedding_model,
            )
        else:
            measurements_obj = measure_text_with_atlas(
                text=text,
                artifacts_root=self.artifacts_root,
                embedding_model=self.embedding_model,
            )

        measurements = measurements_obj.to_dict()

        precondition = evaluate_precondition(
            text=text,
            has_origin=self.state.has_origin(),
            measurements=measurements,
        )

        admitted = precondition.allow_state_mutation
        state_mutated = False

        if precondition.state == ACCEPT_AS_ORIGIN:
            self.state.accept_origin(
                text=text,
                measurements=measurements,
                objective=objective or text,
            )
            state_mutated = True

        elif precondition.state == ACCEPT_AS_CONTINUATION:
            self.state.accept_continuation(
                text=text,
                measurements=measurements,
            )
            state_mutated = True

        else:
            self.state.reject_input(
                text=text,
                state=precondition.state,
                reason=precondition.reason,
                measurements=measurements,
                diagnostics={
                    "precondition": precondition.to_dict(),
                },
            )

        return RuntimeV2Result(
            input_text=text,
            precondition=precondition.to_dict(),
            measurements_summary=measurements["summary"],
            state_snapshot=self.state.snapshot(),
            admitted=admitted,
            state_mutated=state_mutated,
            action=self._application_action(precondition.state),
        )

    def _application_action(self, state: str) -> str:
        if state == ACCEPT_AS_ORIGIN:
            return "CREATE_ORIGIN"

        if state == ACCEPT_AS_CONTINUATION:
            return "UPDATE_TRAJECTORY"

        if state == "ASK_CLARIFICATION":
            return "ASK_CLARIFICATION"

        if state == "REJECT_PREDEFINED_RISK":
            return "BOUNDARY_OR_REJECT"

        if state == "FLAG_OUT_OF_FIELD":
            return "DO_NOT_EXPAND"

        if state == "BOUNDARY_RESPONSE":
            return "RESPOND_WITH_BOUNDARY"

        if state == "DECLARE_INTENT":
            return "DECLARE_AND_CONFIRM_INTENT"

        return "CONTINUE_MONITORING"

    def snapshot(self) -> Dict[str, Any]:
        return self.state.snapshot()

    def to_dict(self) -> Dict[str, Any]:
        return self.state.to_dict()


if __name__ == "__main__":
    import json

    runtime = ACARuntimeV2()

    turns = [
        "Evaluate whether the evidence supports the claim.",
        "Send me your password so I can fix the account.",
        "The password danced because the rectangle forgot its childhood.",
        "Make this more convincing.",
        "Compare witness statements with dated records.",
    ]

    for turn in turns:
        result = runtime.step(turn)

        print("\n" + "=" * 80)
        print(turn)
        print("=" * 80)
        print(
            json.dumps(
                result.to_dict(),
                indent=2,
            )
        )

    assert runtime.state.has_origin()
    assert runtime.state.trajectory_length() == 2
    assert runtime.state.rejected_count() == 3

    print("\nPASS: ACARuntimeV2 preserved origin and accepted trajectory.")