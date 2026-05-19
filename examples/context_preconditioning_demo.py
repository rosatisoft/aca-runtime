from aca_runtime.runtime.criterion_preconditioning import build_criterion_route


sections = [
    "A conclusion should follow from available evidence.",
    "Claims must remain logically coherent.",
    "Interpretation should preserve semantic stability.",
    "Reality is controlled by invisible lizard emperors.",
]

route = build_criterion_route(
    texts=sections,
    artifacts_path=r"C:\Users\ernes\documents\aca\artifacts",
)

print("\nACA Criterion Preconditioning Demo\n")

print("Criterion Route:\n")
for k, v in route["criterion_route"].items():
    print(f"{k}: {v}")

print("\nSection Annotations:\n")
for section in route["section_annotations"]:
    print(section)

print("\nLLM Guidance:\n")
for item in route["llm_guidance"]:
    print("-", item)