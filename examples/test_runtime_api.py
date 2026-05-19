from aca_runtime.runtime import evaluate_runtime


result = evaluate_runtime(
    text="A coherent conclusion should follow from available evidence.",
    artifacts_path=r"C:\Users\ernes\documents\aca\artifacts",
)

print("\nACA Runtime API\n")

for k, v in result["report"].items():
    print(f"{k}: {v}")