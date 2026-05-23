from aca_runtime.runtime.llm_client import call_llm
from aca_runtime.runtime.supervision_modes import supervise_message
from experiments.long_horizon.scenario import SCENARIO
from aca_runtime.runtime.criterion_action_v2 import (
    build_criterion_action,
    build_minimal_prompt,

)



ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"


def build_aca_system_message(result: dict) -> str:
    runtime = result["runtime"]
    trajectory = result["trajectory"]
    declared_shift = result["declared_shift"]
    criterion_response = result["criterion_response"]

    return f"""
You are performing a long-horizon research task under ACA Runtime supervision.

Your goal is to preserve the active criterion across turns.

Current ACA signal:
- Decision: {runtime["decision"]}
- Field: {runtime["semantic_field"]}
- Origin cost: {runtime["origin_cost"]:.4f}
- Trajectory: {trajectory["trajectory_status"]}
- Drift detected: {trajectory["drift_detected"]}
- Criterion preservation: {trajectory["criterion_preservation"]:.4f}
- Declared shift: {declared_shift.get("declared_shift", False)}
- Shift type: {declared_shift.get("shift_type")}

Guidance:
{chr(10).join("- " + g for g in criterion_response["response_guidance"])}

Instructions:
- Do not over-answer.
- Preserve the research objective.
- If the current turn is ambiguous, ask for clarification.
- If the current turn shifts frame, acknowledge the shift.
- If returning to evidence, re-anchor to measurable support.
"""


def main():
    history = []

    baseline_tokens = 0
    aca_tokens = 0

    print("\nACA Experiment 02 — LLM Long-Horizon Supervision\n")

    for idx, message in enumerate(SCENARIO):
        result = supervise_message(
            user_message=message,
            history=history,
            artifacts_path=ARTIFACTS_PATH,
            mode="interactive",
        )

        history = result["history"]

        baseline = call_llm(
            user_message=message,
            system_message=(
                "You are helping with a research task. "
                "Answer naturally and concisely."
            ),
        )

        criterion = build_criterion_action(
            runtime=result["runtime"],
            trajectory=result["trajectory"],
            declared_shift=result["declared_shift"],
        )

        active_objective = (
            history[0]
            if history
            else message
        )

        aca_system_message = build_minimal_prompt(
            criterion,
            objective=active_objective,
        )

        supervised = call_llm(
            user_message=message,
            system_message=
            build_minimal_prompt(
                criterion
            ),
        )

        baseline_tokens += baseline["usage"]["total_tokens"]
        aca_tokens += supervised["usage"]["total_tokens"]

        print("\n========================")
        print("TURN", idx + 1)
        print("========================")

        print("\nUser:")
        print(message)

        print("\nACA Signal:")
        print("Decision:", result["runtime"]["decision"])
        print("Field:", result["runtime"]["semantic_field"])
        print("Trajectory:", result["trajectory"]["trajectory_status"])
        print("Preservation:", round(result["trajectory"]["criterion_preservation"], 4))
        print("Declared Shift:", result["declared_shift"])
        print()

        print(
            "Criterion Check:",
            criterion["mode"]
        )

        print("Meaning:", criterion["meaning"])
        print("Behavior:", criterion["behavior"])

        print("\n--- Baseline LLM ---")
        print(baseline["content"])
        print("Tokens:", baseline["usage"])

        print("\n--- ACA-Supervised LLM ---")
        print(supervised["content"])
        print("Tokens:", supervised["usage"])

    print("\n========================")
    print("TOKEN SUMMARY")
    print("========================")
    print("Baseline tokens:", baseline_tokens)
    print("ACA-supervised tokens:", aca_tokens)
    print("Difference:", aca_tokens - baseline_tokens)

if __name__ == "__main__":
    main()