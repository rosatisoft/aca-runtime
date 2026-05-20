from aca_runtime.runtime.supervision_modes import supervise_message

from experiments.reporter.scenario import SCENARIO


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"

history = []

print("\nACA Experiment 01 — Reporter Mode\n")


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

    print("\n========================")
    print("TURN", idx + 1)
    print("========================")

    print("\nInput:")
    print(message)

    print("\nField:", runtime["semantic_field"])
    print("Decision:", runtime["decision"])

    print(
        "Origin Cost:",
        round(runtime["origin_cost"], 4),
    )

    print(
        "Criterion Preservation:",
        round(
            trajectory["criterion_preservation"],
            4,
        )
    )

    print(
        "Trajectory:",
        trajectory["trajectory_status"],
    )

    print(
        "Declared Shift:",
        declared_shift["declared_shift"],
    )

    if declared_shift["declared_shift"]:
        print(
            "Shift Type:",
            declared_shift["shift_type"],
        )
        print(
            "Target Field:",
            declared_shift["target_field"],
        )
        print(
            "Evidence:",
            declared_shift["evidence"],
        )

    print(
        "Entropy:",
        round(
            trajectory["trajectory_entropy"],
            4,
        )
    )

print("\nExperiment completed.\n")