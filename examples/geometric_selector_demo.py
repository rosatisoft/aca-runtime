from aca_runtime.runtime.geometric_selector import (
    select_best_candidate,
)


ARTIFACTS_PATH = (
    r"C:\Users\ernes\documents\aca\artifacts"
)


OBJECTIVE = (
    "Investigate whether remote work improves productivity using evidence."
)


candidates = [

    "Remote work improves productivity in all cases because people feel freer.",

    "Evidence suggests remote work may improve productivity in some contexts, especially when tasks require focus and organizations provide adequate support.",

    "Remote work is mostly a philosophical question about freedom and meaning.",

    "Remote work productivity cannot be evaluated because productivity is an illusion.",
]


result = select_best_candidate(
    candidates=candidates,
    artifacts_path=ARTIFACTS_PATH,
    objective=OBJECTIVE,
)


print("\nACA Geometric Selector Demo\n")

print("Selected candidate:\n")
print(result["selected"]["candidate"])

print("\nRanking:\n")

for idx, item in enumerate(result["ranked"], start=1):
    report = item["report"]

    print("========================")
    print("Rank:", idx)
    print("Score:", round(item["score"], 4))
    print("Objective Bonus:", round(item["objective_bonus"], 4,))
    print("Decision:", report["decision"])
    print("Field:", report["semantic_field"])
    print("Origin Cost:", round(report["origin_cost"], 4))
    print("Confidence:", round(report["criterion_confidence"], 4))
    print("Text:", item["candidate"])