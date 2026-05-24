from aca_runtime.runtime.text_evaluator import embed_text
from aca_runtime.runtime.foundation_orientation import (
    evaluate_foundation_orientation,
)
from aca_runtime.runtime.api import evaluate_runtime

from experiments.foundation_orientation_diagnostics.scenario import (
    OBJECTIVE,
    EXPANSION_CASES,
    INVERSION_CASES,
    TRAJECTORY_CASES,
)


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"


def evaluate_text_block(text: str) -> dict:
    vector = embed_text(text)

    foundation = evaluate_foundation_orientation(
        vector=vector,
        artifacts_path=ARTIFACTS_PATH,
    )

    runtime = evaluate_runtime(
        text=text,
        artifacts_path=ARTIFACTS_PATH,
    )["report"]

    return {
        "text": text,
        "phi": foundation["foundation_orientation"],
        "decision": runtime["decision"],
        "field": runtime["semantic_field"],
        "origin_cost": runtime["origin_cost"],
        "confidence": runtime["criterion_confidence"],
    }


def print_case(label: str, base_phi: float, result: dict):
    delta = result["phi"] - base_phi

    print("\n--------------------")
    print(label)
    print("--------------------")
    print("Phi:", round(result["phi"], 4))
    print("Delta vs Objective:", round(delta, 4))
    print("Field:", result["field"])
    print("Decision:", result["decision"])
    print("Origin Cost:", round(result["origin_cost"], 4))
    print("Confidence:", round(result["confidence"], 4))
    print("Text:", result["text"])


def run_group(title: str, cases: list[str]):
    print("\n==============================")
    print(title)
    print("==============================")

    objective_result = evaluate_text_block(OBJECTIVE)
    base_phi = objective_result["phi"]

    print("\nObjective Phi:", round(base_phi, 4))

    previous_phi = None

    for idx, text in enumerate(cases, start=1):
        result = evaluate_text_block(text)

        print_case(
            label=f"Case {idx}",
            base_phi=base_phi,
            result=result,
        )

        if previous_phi is not None:
            print(
                "Delta vs Previous:",
                round(result["phi"] - previous_phi, 4),
            )

        previous_phi = result["phi"]


def main():
    run_group(
        "Experiment A — Expansion",
        EXPANSION_CASES,
    )

    run_group(
        "Experiment B — Inversion",
        INVERSION_CASES,
    )

    run_group(
        "Experiment C — Trajectory",
        TRAJECTORY_CASES,
    )


if __name__ == "__main__":
    main()