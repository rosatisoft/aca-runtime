from aca_runtime.runtime.loader import load_artifacts_atlas
from aca_runtime.runtime.text_evaluator import evaluate_text


atlas = load_artifacts_atlas(
    r"C:\Users\ernes\documents\aca\artifacts"
)

text = "A coherent conclusion should follow from available evidence."

result = evaluate_text(text, atlas)

print("\nACA Text Runtime Result\n")
print("Input:", result["input_text"])
print("Embedding model:", result["embedding_model"])
print("Embedding dim:", result["embedding_dim"])
print("Best field:", result["best_field"])
print("Second best field:", result["second_best_field"])
print("Origin cost:", result["origin_cost"])
print("Field margin:", result["field_margin"])
print("Ambiguity:", result["ambiguity_status"])
print("Policy:", result["policy"])

print("\nField analysis:\n")
for field_name, field_data in result["fields"].items():
    print(
        field_name,
        "| cost =", round(field_data["origin_cost"], 6),
        "| policy =", field_data["policy"],
    )