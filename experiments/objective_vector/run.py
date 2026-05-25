from aca_runtime.runtime.text_evaluator import embed_text
from aca_runtime.runtime.api import evaluate_runtime
from aca_runtime.runtime.foundation_orientation import (
    evaluate_foundation_orientation,
)

from experiments.objective_vector.scenario import (
    OBJECTIVE,
    TURNS,
)


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"


def cosine_similarity(a, b):
    numerator = float(a @ b)
    denominator = float((a @ a) ** 0.5 * (b @ b) ** 0.5)

    if denominator == 0:
        return 0.0

    return numerator / denominator


def evaluate_turn(
    text: str,
    goal_vector,
    previous_phi=None,
):
    vector = embed_text(text)

    runtime = evaluate_runtime(
        text=text,
        artifacts_path=ARTIFACTS_PATH,
    )["report"]

    foundation = evaluate_foundation_orientation(
        vector=vector,
        artifacts_path=ARTIFACTS_PATH,
    )

    phi = foundation["foundation_orientation"]

    delta_phi = None

    if previous_phi is not None:
        delta_phi = phi - previous_phi

    goal_alignment = cosine_similarity(
        vector,
        goal_vector,
    )

    return {
        "text": text,
        "field": runtime["semantic_field"],
        "decision": runtime["decision"],
        "origin_cost": runtime["origin_cost"],
        "confidence": runtime["criterion_confidence"],
        "phi": phi,
        "delta_phi": delta_phi,
        "goal_alignment": goal_alignment,
    }


def main():
    print("\nExperiment 04 — Geometric Objective Persistence\n")

    goal_vector = embed_text(OBJECTIVE)

    print("Objective:")
    print(OBJECTIVE)

    print("\nGoal vector created from objective.")
    print("Text objective will not be repeated per turn.")
    print()

    previous_phi = None

    for idx, turn in enumerate(TURNS, start=1):
        result = evaluate_turn(
            text=turn,
            goal_vector=goal_vector,
            previous_phi=previous_phi,
        )

        previous_phi = result["phi"]

        print("\n========================")
        print("TURN", idx)
        print("========================")
        print("Input:", result["text"])
        print("Field:", result["field"])
        print("Decision:", result["decision"])
        print("Origin Cost:", round(result["origin_cost"], 4))
        print("Confidence:", round(result["confidence"], 4))
        print("Goal Alignment:", round(result["goal_alignment"], 4))
        print("Phi:", round(result["phi"], 4))

        if result["delta_phi"] is not None:
            print("Delta Phi:", round(result["delta_phi"], 4))
        else:
            print("Delta Phi: initial")


if __name__ == "__main__":
    main()