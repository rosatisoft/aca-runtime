from aca_runtime.runtime.criterion_response import build_criterion_response
from aca_runtime.runtime.llm_client import call_llm
from aca_runtime.runtime.api import (
    evaluate_runtime,
    evaluate_runtime_trajectory,
)


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"

messages = [
    "I want to understand a problem using evidence.",
    "What if evidence is unnecessary?",
    "Reality is controlled by invisible lizard emperors.",
]


history = []

print("\nLLM Baseline vs ACA-Supervised Demo\n")

for idx, user_message in enumerate(messages):
    history.append(user_message)

    print("\n==============================")
    print("TURN", idx + 1)
    print("==============================")

    print("\nUser:")
    print(user_message)

    baseline = call_llm(
        user_message=user_message,
        system_message="Answer naturally and concisely.",
    )

    runtime = evaluate_runtime(
        text=user_message,
        artifacts_path=ARTIFACTS_PATH,
    )

    trajectory = evaluate_runtime_trajectory(
        texts=history,
        artifacts_path=ARTIFACTS_PATH,
    )

    criterion_response = build_criterion_response(
        user_message=user_message,
        runtime_report=runtime["report"],
        trajectory_report=trajectory["report"],
    )

    aca_system_message = f"""
You are an assistant supervised by ACA Runtime.

Use the following criterion signals before answering.

Runtime signal:
{criterion_response["signal_summary"]}

Trajectory signal:
{criterion_response["trajectory_summary"]}

Guidance:
{chr(10).join("- " + g for g in criterion_response["response_guidance"])}

If clarification is recommended, ask a clarifying question instead of continuing with an unsupported answer.
"""

    supervised = call_llm(
        user_message=user_message,
        system_message=aca_system_message,
    )

    print("\n--- Baseline LLM ---")
    print(baseline["content"])
    print("Tokens:", baseline["usage"])

    print("\n--- ACA Criterion Response ---")
    print(criterion_response["assistant_message"])

    print("\n--- ACA-Supervised LLM ---")
    print(supervised["content"])
    print("Tokens:", supervised["usage"])

    print("\n--- ACA Signals ---")
    print("Decision:", runtime["report"]["decision"])
    print("Field:", runtime["report"]["semantic_field"])
    print("Origin cost:", runtime["report"]["origin_cost"])
    print("Trajectory:", trajectory["report"]["trajectory_status"])