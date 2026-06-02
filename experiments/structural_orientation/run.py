from statistics import mean

import numpy as np

from aca_runtime.runtime.text_evaluator import embed_text

from experiments.structural_orientation.scenario import (
    PRESERVING,
    DEGRADING,
    FICTIONAL,
    HYPOTHETICAL,
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


def build_orientation_centroids():
    centroids = {}

    preserving_vectors = [
        normalize(embed_text(text))
        for text in PRESERVING
    ]

    degrading_vectors = [
        normalize(embed_text(text))
        for text in DEGRADING
    ]

    centroids["preserving"] = normalize(
        np.mean(
            preserving_vectors,
            axis=0,
        )
    )

    centroids["degrading"] = normalize(
        np.mean(
            degrading_vectors,
            axis=0,
        )
    )

    fictional_vectors = [
        normalize(embed_text(text))
        for text in FICTIONAL
    ]

    hypothetical_vectors = [
        normalize(embed_text(text))
        for text in HYPOTHETICAL
    ]

    centroids["fictional"] = normalize(
        np.mean(
            fictional_vectors,
            axis=0,
        )
    )

    centroids["hypothetical"] = normalize(
        np.mean(
            hypothetical_vectors,
            axis=0,
        )
    )

    return centroids


def classify_orientation(text, centroids):
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

    print("\nSTRUCTURAL ORIENTATION")
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

    if margin < 0.05:
        interpretation = f"AMBIGUOUS ({top['intent']})"
    else:
        interpretation = top["intent"]

    print("INTERPRETATION:", interpretation)

    print("\nTOP:", top["intent"])
    print("MARGIN:", round(margin, 4))


def main():
    print("\nStructural Orientation Diagnostics v0.1\n")

    centroids = build_orientation_centroids()

    print("Structural centroids created:")
    for intent in centroids:
        print("-", intent)


    print("\n==============================")
    print("TEST CASES")
    print("==============================")

    for text in TEST_CASES:
        ranked = classify_orientation(
            text,
            centroids,
        )

        print_ranking(
            text,
            ranked,
        )


if __name__ == "__main__":
    main()