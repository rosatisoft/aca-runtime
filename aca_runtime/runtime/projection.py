import numpy as np


def origin_cost(vector: np.ndarray, basis: np.ndarray) -> float:
    """
    Computes O(z) = ||v - P_S(v)||^2.
    basis must be an orthonormal matrix with shape (dim, k).
    """
    v = vector.reshape(-1, 1)
    projection = basis @ (basis.T @ v)
    residual = v - projection
    return float(np.linalg.norm(residual) ** 2)