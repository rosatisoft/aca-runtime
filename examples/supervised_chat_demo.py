from aca_runtime.runtime.supervised_chat import (
    SupervisedChat,
)

chat = SupervisedChat(
    artifacts_path=r"C:\Users\ernes\documents\aca\artifacts"
)

messages = [
    "I want to understand a problem using evidence.",
    "What if evidence is unnecessary?",
    "Reality is controlled by invisible lizard emperors."
]

for idx, msg in enumerate(messages):

    result = chat.step(msg)

    print("\nTURN", idx + 1)

    print("User:")
    print(result["user"])

    print("\nRuntime:")
    print(result["runtime"])

    print("\nTrajectory:")
    print(result["trajectory"])

    print("\nAssistant Message:")
    print(result["assistant"]["assistant_message"])

    print("\nCriterion Details:")
    print("Signal:", result["assistant"]["signal_summary"])
    print("Trajectory:", result["assistant"]["trajectory_summary"])
    print("Guidance:")
    for item in result["assistant"]["response_guidance"]:
        print("-", item)