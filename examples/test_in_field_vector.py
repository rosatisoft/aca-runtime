from aca_runtime.runtime.loader import load_artifacts_atlas
from aca_runtime.runtime.evaluator import evaluate_vector


atlas = load_artifacts_atlas(
    r"C:\Users\ernes\documents\aca\artifacts"
)

field = atlas["fields"]["foundational"]

# Tomamos un vector directamente del subespacio foundational
vector = field["basis"][:, 0]

result = evaluate_vector(vector, atlas)

print("\nACA Runtime In-Field Test\n")
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
        "| cost =", round(field_data["origin_cost"], 12),
        "| policy =", field_data["policy"],
    )