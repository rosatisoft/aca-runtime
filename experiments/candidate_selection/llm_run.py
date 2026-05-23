from aca_runtime.runtime.llm_client import call_llm

from aca_runtime.runtime.geometric_selector import (
    select_best_candidate,
)

from experiments.candidate_selection.scenario import (
    USER_MESSAGE,
    OBJECTIVE,
)


ARTIFACTS_PATH = (
    r"C:\Users\ernes\documents\aca\artifacts"
)


def generate_llm_candidates(
    user_message: str,
    n: int = 4,
) -> list[str]:

    candidates = []

    for idx in range(n):

        result = call_llm(
            user_message=(
                f"{user_message}\n\n"
                f"Generate candidate answer #{idx + 1}. "
                f"Keep it concise."
            ),
            system_message=(
                "You are generating candidate answers. "
                "Do not mention that this is a candidate."
            ),
        )

        candidates.append(
            result["content"]
        )

    return candidates


def main():

    print(
        "\nACA Experiment 03 — LLM Candidate Selection\n"
    )

    print(
        "User:\n"
    )

    print(
        USER_MESSAGE
    )

    print(
        "\nGenerating candidates...\n"
    )

    candidates = generate_llm_candidates(
        user_message=USER_MESSAGE,
        n=4,
    )

    result = select_best_candidate(
        candidates=candidates,
        artifacts_path=ARTIFACTS_PATH,
        objective=OBJECTIVE,
    )

    print(
        "\n=================="
    )
    print(
        "SELECTED"
    )
    print(
        "==================\n"
    )

    print(
        result["selected"]["candidate"]
    )

    print(
        "\n=================="
    )
    print(
        "RANKING"
    )
    print(
        "=================="
    )

    for idx, item in enumerate(
        result["ranked"],
        start=1,
    ):

        report = item["report"]

        print()
        print(
            "Rank:",
            idx,
        )
        print(
            "Score:",
            round(
                item["score"],
                4,
            ),
        )
        print(
            "Objective Bonus:",
            round(
                item["objective_bonus"],
                4,
            ),
        )
        print(
            "Candidate Orientation:",
            round(
                item[
                    "candidate_orientation"
                ],
                4,
            ),
        )

        print(
            "Objective Orientation:",
            round(
                item[
                    "objective_orientation"
                ],
                4,
            ),
        )

        print(
            "Foundation Delta:",
            round(
                item[
                    "foundation_delta"
                ],
                4,
            ),
        )

        print(
            "Foundation Preserved:",
            item["foundation_preserved"],
        )

        print(
            "Decision:",
            report["decision"],
        )
        print(
            "Field:",
            report["semantic_field"],
        )
        print(
            "Origin Cost:",
            round(
                report["origin_cost"],
                4,
            ),
        )
        print(
            "Confidence:",
            round(
                report["criterion_confidence"],
                4,
            ),
        )
        print(
            "Candidate:"
        )
        print(
            item["candidate"]
        )


if __name__ == "__main__":
    main()