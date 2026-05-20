from aca_runtime.runtime.supervision_modes import supervise_message


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"

history = []

messages = [
    "I want to understand a problem using evidence.",
    "What if evidence is unnecessary?",
    "Reality is controlled by invisible lizard emperors.",
]

for mode in ["report", "warning", "interactive", "moderator"]:
    print("\n==============================")
    print("MODE:", mode)
    print("==============================")

    history = []

    for msg in messages:
        result = supervise_message(
            user_message=msg,
            history=history,
            artifacts_path=ARTIFACTS_PATH,
            mode=mode,
        )

        history = result["history"]

        print("\nUser:", msg)
        print("Decision:", result["runtime"]["decision"])
        print("Trajectory:", result["trajectory"]["trajectory_status"])
        print("Intervention:", result["intervention"])