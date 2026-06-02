import json

import numpy as np

from aca_runtime.runtime.text_evaluator import embed_text

from experiments.criterion_geometry.scenario import (
    PHYSICAL_FACTUAL,
    PHYSICAL_FICTIONAL,
    PHYSICAL_HYPOTHETICAL,

    RATIONAL_COHERENT,
    RATIONAL_FRAGMENTED,

    INTENT_INVESTIGATE,
    INTENT_TEACH,
    INTENT_EXPLOIT,

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

        "physical": {
            "factual": centroid(PHYSICAL_FACTUAL),
            "fictional": centroid(PHYSICAL_FICTIONAL),
            "hypothetical": centroid(PHYSICAL_HYPOTHETICAL),
        },

        "rational": {
            "coherent": centroid(RATIONAL_COHERENT),
            "fragmented": centroid(RATIONAL_FRAGMENTED),
        },

        "intentional": {
            "investigate": centroid(INTENT_INVESTIGATE),
            "teach": centroid(INTENT_TEACH),
            "exploit": centroid(INTENT_EXPLOIT),
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

        "physical": score_plane(
            vector,
            planes["physical"],
        ),

        "rational": score_plane(
            vector,
            planes["rational"],
        ),

        "intentional": score_plane(
            vector,
            planes["intentional"],
        ),
    }


def main():
    print("\nExperiment 08 — Criterion Planes v0.2\n")

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