from aca_runtime.runtime.text_evaluator import embed_text
from aca_runtime.runtime.llm_client import call_llm
from aca_runtime.runtime.geometric_selector import select_best_candidate

from experiments.objective_vector.scenario import (
    OBJECTIVE,
    TURNS,
)


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"
ALIGNMENT_THRESHOLD = 0.45


def cosine_similarity(a, b):
    numerator = float(a @ b)
    denominator = float((a @ a) ** 0.5 * (b @ b) ** 0.5)

    if denominator == 0:
        return 0.0

    return numerator / denominator


def generate_candidates(turn: str, mode: str, n: int = 4) -> list[str]:
    candidates = []

    for idx in range(n):
        if mode == "reanchor":
            system_message = (
                "Generate a concise answer that reconnects the user request "
                "to the active research task. Do not ask for the objective. "
                "Preserve evidence, measurable outcomes, and supported conclusions."
            )
        else:
            system_message = (
                "Generate a concise answer to the user request."
            )

        result = call_llm(
            user_message=turn,
            system_message=system_message,
        )

        candidates.append(result["content"])

    return candidates


def main():
    print("\nExperiment 05 — Criterion Operating Layer v0.1\n")

    goal_vector = embed_text(OBJECTIVE)
    context = ""

    print("Objective:")
    print(OBJECTIVE)

    for idx, turn in enumerate(TURNS, start=1):
        evaluation_text = context + "\n" + turn
        alignment = cosine_similarity(
            embed_text(evaluation_text),
            goal_vector,
        )

        mode = "direct"

        if alignment < ALIGNMENT_THRESHOLD:
            mode = "reanchor"

        candidates = generate_candidates(
            turn=turn,
            mode=mode,
            n=4,
        )

        result = select_best_candidate(
            candidates=candidates,
            artifacts_path=ARTIFACTS_PATH,
            objective=OBJECTIVE,
        )

        selected = result["selected"]["candidate"]

        context += "\n" + selected

        print("\n========================")
        print("TURN", idx)
        print("========================")
        print("Input:", turn)
        print("Goal Alignment:", round(alignment, 4))
        print("Mode:", mode)
        print("\nTop Ranked Response:")
        print(selected)

        print("\nRanking:")
        for rank, item in enumerate(result["ranked"], start=1):
            print(
                rank,
                "| score:",
                round(item["score"], 4),
                "| objective:",
                round(item["objective_bonus"], 4),
                "| field:",
                item["report"]["semantic_field"],
                "| decision:",
                item["report"]["decision"],
            )


if __name__ == "__main__":
    main()