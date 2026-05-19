import numpy as np

from aca_runtime.runtime.evaluator import evaluate_vector


dim = 5

basis = np.eye(dim)[:, :2]

atlas = {
    "fields": {
        "foundational": {
            "basis": basis,
            "threshold": 0.35,
        }
    }
}

vector = np.array([1, 0, 0, 0, 0], dtype=float)

result = evaluate_vector(vector, atlas)

print(result)