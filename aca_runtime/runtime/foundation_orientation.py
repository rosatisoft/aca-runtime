from pathlib import Path

import numpy as np


def normalize_vector(
    vector: np.ndarray,
    epsilon: float = 1e-12,
) -> np.ndarray:
    norm = np.linalg.norm(vector)

    if norm < epsilon:
        return vector

    return vector / norm


def load_foundation_directions(
    artifacts_path: str,
) -> np.ndarray:
    foundational_dir = (
        Path(artifacts_path)
        / "foundational"
    )

    directions_path = (
        foundational_dir
        / "invariant_directions.npy"
    )

    if not directions_path.exists():
        raise FileNotFoundError(
            f"Missing invariant directions: {directions_path}"
        )

    return np.load(
        directions_path
    )


def evaluate_foundation_orientation(
    vector: np.ndarray,
    artifacts_path: str,
) -> dict:
    directions = load_foundation_directions(
        artifacts_path
    )

    z = normalize_vector(
        np.asarray(
            vector,
            dtype=np.float64,
        )
    )

    scores = []

    for direction in directions:

        d = normalize_vector(
            np.asarray(
                direction,
                dtype=np.float64,
            )
        )

        scores.append(
            float(
                np.dot(
                    z,
                    d,
                )
            )
        )

    if not scores:
        aggregate = 0.0
    else:
        aggregate = float(
            np.mean(
                scores
            )
        )

    return {
        "foundation_orientation": aggregate,
        "invariant_scores": scores,
        "preserved": aggregate > 0.0,
    }