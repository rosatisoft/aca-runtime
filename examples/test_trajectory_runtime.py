from aca_runtime.runtime.trajectory_runtime import (
    evaluate_trajectory,
)


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

print("\nACA Trajectory Runtime\n")

print("Trajectory status:", result["trajectory_status"])
print("Drift detected:", result["drift_detected"])
print("Criterion preservation:", result["criterion_preservation"])
print("Trajectory entropy:", result["trajectory_entropy"])

print("\nField sequence:\n")

for idx, field in enumerate(result["field_sequence"]):
    print(idx, "->", field)

print("\nDrift events:\n")

for event in result["drift_events"]:
    print(event)