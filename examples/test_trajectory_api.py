from aca_runtime.runtime import evaluate_runtime_trajectory


texts = [
    "A conclusion should follow from available evidence.",
    "Claims must remain logically coherent.",
    "Interpretation should preserve semantic stability.",
    "Reality is controlled by invisible lizard emperors.",
]

result = evaluate_runtime_trajectory(
    texts=texts,
    artifacts_path=r"C:\Users\ernes\documents\aca\artifacts",
)

print("\nACA Trajectory API\n")

for k, v in result["report"].items():
    print(f"{k}: {v}")