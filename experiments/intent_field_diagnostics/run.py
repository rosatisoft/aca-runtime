from statistics import mean

import numpy as np

from aca_runtime.runtime.text_evaluator import embed_text

from experiments.intent_field_diagnostics.scenario import (
    INTENT_EXAMPLES,
    TEST_CASES,
)


def normalize(vector):
    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector

    return vector / norm


def cosine_similarity(a, b):
    a = normalize(a)
    b = normalize(b)

    return float(np.dot(a, b))


def build_intent_centroids():
    centroids = {}

    for intent, examples in INTENT_EXAMPLES.items():
        vectors = [
            normalize(embed_text(example))
            for example in examples
        ]

        centroid = normalize(
            np.mean(
                vectors,
                axis=0,
            )
        )

        centroids[intent] = centroid

    return centroids


def classify_intent(text, centroids):
    vector = normalize(
        embed_text(text)
    )

    scores = []

    for intent, centroid in centroids.items():
        scores.append(
            {
                "intent": intent,
                "score": cosine_similarity(
                    vector,
                    centroid,
                ),
            }
        )

    ranked = sorted(
        scores,
        key=lambda item: item["score"],
        reverse=True,
    )

    return ranked


def print_ranking(text, ranked):
    print("\n==============================")
    print("TEXT")
    print("==============================")
    print(text)

    print("\nINTENT RANKING")
    for item in ranked:
        print(
            item["intent"],
            round(
                item["score"],
                4,
            ),
        )

    top = ranked[0]
    second = ranked[1]

    margin = top["score"] - second["score"]

    print("\nTOP:", top["intent"])
    print("MARGIN:", round(margin, 4))


def main():
    print("\nIntent Field Diagnostics v0.1\n")

    centroids = build_intent_centroids()

    print("Intent centroids created:")
    for intent in centroids:
        print("-", intent)

    print("\n==============================")
    print("SELF-CHECK")
    print("==============================")

    for intent, examples in INTENT_EXAMPLES.items():
        scores = []

        for example in examples:
            ranked = classify_intent(
                example,
                centroids,
            )

            scores.append(
                ranked[0]["intent"] == intent
            )

        accuracy = mean(scores)

        print(
            intent,
            "self-check:",
            round(
                accuracy,
                2,
            ),
        )

    print("\n==============================")
    print("TEST CASES")
    print("==============================")

    for text in TEST_CASES:
        ranked = classify_intent(
            text,
            centroids,
        )

        print_ranking(
            text,
            ranked,
        )


if __name__ == "__main__":
    main()