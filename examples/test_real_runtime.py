import numpy as np

from aca_runtime.runtime.loader import load_artifacts_atlas
from aca_runtime.runtime.evaluator import evaluate_vector


atlas = load_artifacts_atlas(
    r"C:\Users\ernes\documents\aca\artifacts"
)

dim = 1536

# Simulación simple
# después conectaremos embeddings reales

vector = np.random.randn(dim)
vector = vector / np.linalg.norm(vector)

result = evaluate_vector(vector, atlas)

print("\nACA Runtime Result\n")

print("Best field:", result["best_field"])
print("Origin cost:", result["origin_cost"])
print("Policy:", result["policy"])
print("Second best field:", result["second_best_field"])
print("Field margin:", result["field_margin"])
print("Ambiguity:", result["ambiguity_status"])

print("\nField analysis:\n")

for field_name, field_data in result["fields"].items():
    print(
        field_name,
        "| cost =", round(field_data["origin_cost"], 6),
        "| policy =", field_data["policy"],
    )