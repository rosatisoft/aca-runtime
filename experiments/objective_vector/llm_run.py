from aca_runtime.runtime.text_evaluator import embed_text

from experiments.objective_vector.scenario import (
    OBJECTIVE,
    TURNS,
)

from aca_runtime.runtime.llm_client import call_llm


THRESHOLD = 0.30


def cosine_similarity(a, b):
    numerator = float(a @ b)

    denominator = float(
        (a @ a) ** 0.5
        *
        (b @ b) ** 0.5
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


def build_guidance(
    alignment,
):
    if alignment < THRESHOLD:
        return (
            "Goal alignment is low. "
            "Re-anchor to active objective. "
            "Do not reconstruct objective."
        )

    return (
        "Maintain active direction."
    )


def main():

    print(
        "\nExperiment 04B — Goal Vector Guidance\n"
    )

    goal_vector = embed_text(
        OBJECTIVE
    )

    context = ""

    for idx, turn in enumerate(
        TURNS,
        start=1,
    ):

        alignment = cosine_similarity(
            embed_text(
                context + turn
            ),
            goal_vector,
        )

        guidance = build_guidance(
            alignment
        )

        print(
            "\n===================="
        )

        print(
            "TURN",
            idx,
        )

        print(
            "Input:",
            turn,
        )

        print(
            "Alignment:",
            round(
                alignment,
                4,
            ),
        )

        print(
            "Guidance:",
            guidance,
        )

        response = call_llm(
            user_message=turn,
            system_message=guidance,
        )

        print(
            "\nLLM:"
        )

        print(
            response["content"]
        )

        context += (
            "\n"
            + response["content"]
        )


if __name__ == "__main__":
    main()