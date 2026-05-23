from experiments.document_preconditioning.scenario import TEXT

from aca_runtime.runtime.criterion_preconditioning import (
    build_criterion_route,
)


def split_text(
    text,
    chunk=400,
):

    return [
        text[i:i+chunk]
        for i in range(
            0,
            len(text),
            chunk,
        )
    ]


def main():

    sections = split_text(TEXT)

    route_result = build_criterion_route(
        texts=sections,
        artifacts_path=r"C:\Users\ernes\documents\aca\artifacts",
    )

    route = route_result["section_annotations"]

    from experiments.document_preconditioning.preconditioning import (
        build_preconditioning_prompt
    )

    prompt = build_preconditioning_prompt(
        route
    )

    print("\n====================")
    print("DOCUMENT ROUTE")
    print("====================\n")

    for item in route:

        print(
            f"Section {item['section']}"
        )

        print("Field:", item["best_field"])
        print("Policy:", item["policy"])
        print("Risk:", item["risk"])
        print("Ambiguity:", item["ambiguity"])

        if "field" in item:
            print(
                "Field:",
                item["field"]
            )

        print()

    print("\n====================")
    print("PRECONDITIONING")
    print("====================\n")

    print(prompt)


if __name__ == "__main__":
    main()