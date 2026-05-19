from aca_runtime.runtime.trajectory_runtime import evaluate_trajectory
from aca_runtime.runtime.trajectory_report import build_trajectory_report


texts = [
    "A conclusion should follow from available evidence.",
    "Claims must remain logically coherent.",
    "Interpretation should preserve semantic stability.",
    "Reality is controlled by invisible lizard emperors.",
]

result = evaluate_trajectory(
    texts=texts,
    artifacts_path=r"C:\Users\ernes\documents\aca\artifacts",
    drift_threshold=0.20,
)

report = build_trajectory_report(result)

print("\nACA Trajectory Report\n")

for k, v in report.items():
    print(f"{k}: {v}")