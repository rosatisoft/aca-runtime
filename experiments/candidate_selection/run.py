from experiments.candidate_selection.scenario import (
    USER_MESSAGE,
    OBJECTIVE,
)

from experiments.candidate_selection.candidate_generator import (
    generate_candidates,
)

from aca_runtime.runtime.geometric_selector import (
    select_best_candidate,
)


ARTIFACTS_PATH = (
    r"C:\Users\ernes\documents\aca\artifacts"
)


def main():

    print(
        "\nACA Experiment 03"
    )

    print(
        "\nUser:\n"
    )

    print(
        USER_MESSAGE
    )

    candidates = (
        generate_candidates()
    )

    result = (
        select_best_candidate(
            candidates=candidates,
            artifacts_path=ARTIFACTS_PATH,
            objective=OBJECTIVE,
        )
    )

    print(
        "\n=================="
    )

    print(
        "SELECTED"
    )

    print(
        "=================="
    )

    print(
        result[
            "selected"
        ][
            "candidate"
        ]
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
        result[
            "ranked"
        ],
        start=1,
    ):

        r = item["report"]

        print()

        print(
            idx,
            "|",
            round(
                item[
                    "score"
                ],
                4,
            ),
        )

        print(
            "Decision:",
            r[
                "decision"
            ],
        )

        print(
            "Field:",
            r[
                "semantic_field"
            ],
        )

        print(
            "Objective:",
            round(
                item[
                    "objective_bonus"
                ],
                4,
            ),
        )

        print(
            item[
                "candidate"
            ],
        )


if __name__ == "__main__":
    main()