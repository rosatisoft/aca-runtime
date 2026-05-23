from aca_runtime.runtime.supervision_modes import supervise_message

from experiments.long_horizon.scenario import SCENARIO
from experiments.long_horizon.metrics import metrics


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"


def is_recovery(result: dict) -> bool:
    declared_shift = result["declared_shift"]
    trajectory = result["trajectory"]

    return (
        declared_shift.get("declared_shift", False)
        and trajectory["drift_detected"]
    )


def is_unsupported_claim(result: dict) -> bool:
    runtime = result["runtime"]

    return (
        runtime["semantic_field"] == "factual"
        and runtime["origin_cost"] > 0.75
    )


def main():
    history = []

    print("\nACA Experiment 02 — Long-Horizon Criterion Preservation\n")

    for idx, message in enumerate(SCENARIO):

        result = supervise_message(
            user_message=message,
            history=history,
            artifacts_path=ARTIFACTS_PATH,
            mode="report",
        )

        history = result["history"]

        runtime = result["runtime"]
        trajectory = result["trajectory"]
        declared_shift = result["declared_shift"]

        metrics["turns"] += 1

        if trajectory["drift_detected"]:
            metrics["drift_count"] += 1

        if declared_shift.get("declared_shift", False):
            metrics["declared_shift_count"] += 1

        if is_recovery(result):
            metrics["recovery_count"] += 1

        if "CLARIFY" in runtime["decision"]:
            metrics["clarification_events"] += 1

        if is_unsupported_claim(result):
            metrics["unsupported_claims"] += 1

        metrics["criterion_preservation"].append(
            trajectory["criterion_preservation"]
        )

        print("\n========================")
        print("TURN", idx + 1)
        print("========================")

        print("\nInput:")
        print(message)

        print("\nField:", runtime["semantic_field"])
        print("Decision:", runtime["decision"])
        print("Origin Cost:", round(runtime["origin_cost"], 4))

        print(
            "Preservation:",
            round(
                trajectory["criterion_preservation"],
                4,
            )
        )

        print("Trajectory:", trajectory["trajectory_status"])
        print("Drift Detected:", trajectory["drift_detected"])

        print(
            "Declared Shift:",
            declared_shift.get("declared_shift", False),
        )

        if declared_shift.get("declared_shift", False):
            print("Shift Type:", declared_shift["shift_type"])
            print("Evidence:", declared_shift["evidence"])

        print("Recovery:", is_recovery(result))
        print("Unsupported Claim:", is_unsupported_claim(result))

    preservation_values = metrics["criterion_preservation"]

    avg_preservation = (
        sum(preservation_values) / len(preservation_values)
        if preservation_values
        else 0.0
    )

    print("\n========================")
    print("SUMMARY")
    print("========================")

    print("Turns:", metrics["turns"])
    print("Drift Count:", metrics["drift_count"])
    print("Declared Shift Count:", metrics["declared_shift_count"])
    print("Recovery Count:", metrics["recovery_count"])
    print("Clarification Events:", metrics["clarification_events"])
    print("Unsupported Claims:", metrics["unsupported_claims"])
    print("Average Preservation:", round(avg_preservation, 4))


if __name__ == "__main__":
    main()