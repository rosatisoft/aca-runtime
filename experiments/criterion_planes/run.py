import json

import numpy as np

from aca_runtime.runtime.text_evaluator import embed_text

from experiments.criterion_planes.scenario import (
    REFERENCE_FACTUAL,
    REFERENCE_FICTIONAL,
    REFERENCE_HYPOTHETICAL,
    STRUCTURE_PRESERVING,
    STRUCTURE_DEGRADING,
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


def centroid(texts):
    vectors = [
        normalize(embed_text(text))
        for text in texts
    ]

    return normalize(
        np.mean(
            vectors,
            axis=0,
        )
    )


def build_plane_centroids():
    return {
        "reference": {
            "factual": centroid(REFERENCE_FACTUAL),
            "fictional": centroid(REFERENCE_FICTIONAL),
            "hypothetical": centroid(REFERENCE_HYPOTHETICAL),
        },
        "structure": {
            "preserving": centroid(STRUCTURE_PRESERVING),
            "degrading": centroid(STRUCTURE_DEGRADING),
        },
    }


def score_plane(vector, plane_centroids):
    scores = {}

    for name, plane_centroid in plane_centroids.items():
        scores[name] = cosine_similarity(
            vector,
            plane_centroid,
        )

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    top_name, top_score = ranked[0]
    second_name, second_score = ranked[1]

    return {
        "scores": {
            key: round(value, 4)
            for key, value in scores.items()
        },
        "top": top_name,
        "top_score": round(top_score, 4),
        "margin": round(top_score - second_score, 4),
    }


def build_criterion_profile(text, planes):
    vector = normalize(
        embed_text(text)
    )

    return {
        "input": text,
        "reference": score_plane(
            vector,
            planes["reference"],
        ),
        "structure": score_plane(
            vector,
            planes["structure"],
        ),
    }


def main():
    print("\nExperiment 07 — Criterion Planes v0.1\n")

    planes = build_plane_centroids()

    for text in TEST_CASES:
        profile = build_criterion_profile(
            text,
            planes,
        )

        print("\n==============================")
        print("INPUT")
        print("==============================")
        print(text)

        print("\nCRITERION PROFILE")
        print(
            json.dumps(
                profile,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()