from aca_runtime.runtime.loader import load_artifacts_atlas


atlas = load_artifacts_atlas(
    r"C:\Users\ernes\documents\aca\artifacts"
)

print("Loaded fields:")

for field_name, field in atlas["fields"].items():
    print(
        field_name,
        field["basis"].shape,
        "threshold:",
        field["threshold"],
        "rank:",
        field["metadata"].get("svd_rank"),
    )