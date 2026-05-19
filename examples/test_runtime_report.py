from aca_runtime.runtime.loader import load_artifacts_atlas
from aca_runtime.runtime.runtime_report import build_runtime_report
from aca_runtime.runtime.text_evaluator import evaluate_text


atlas = load_artifacts_atlas(
    r"C:\Users\ernes\documents\aca\artifacts"
)

text = "A coherent conclusion should follow from available evidence."

result = evaluate_text(text, atlas)

report = build_runtime_report(result)

print("\nACA Runtime Report\n")

for k, v in report.items():
    print(f"{k}: {v}")