from .projection import origin_cost
from .policy import decide_policy


def evaluate_vector(vector, atlas, ambiguity_margin: float = 0.05):
    """
    Evaluate a vector against all ACA semantic fields.

    Returns:
    - best_field
    - origin_cost
    - policy
    - field_margin
    - ambiguity_status
    - per-field analysis
    """

    results = {}

    for field_name, field_data in atlas["fields"].items():
        cost = origin_cost(vector, field_data["basis"])
        threshold = field_data["threshold"]

        results[field_name] = {
            "origin_cost": cost,
            "threshold": threshold,
            "policy": decide_policy(cost, threshold),
        }

    ranked_fields = sorted(
        results.items(),
        key=lambda item: item[1]["origin_cost"],
    )

    best_field, best_data = ranked_fields[0]

    if len(ranked_fields) > 1:
        second_field, second_data = ranked_fields[1]
        field_margin = second_data["origin_cost"] - best_data["origin_cost"]
    else:
        second_field = None
        field_margin = None

    ambiguity_status = "CLEAR"

    if field_margin is not None and field_margin < ambiguity_margin:
        ambiguity_status = "AMBIGUOUS"

    final_policy = best_data["policy"]

    if ambiguity_status == "AMBIGUOUS":
        if final_policy == "ALLOW":
            final_policy = "ALLOW_LIGHT"
        elif final_policy == "CLARIFY":
            final_policy = "AMBIGUOUS_CLARIFY"
        elif final_policy == "FLAG_DRIFT":
            final_policy = "AMBIGUOUS_DRIFT"

    return {
        "best_field": best_field,
        "second_best_field": second_field,
        "origin_cost": best_data["origin_cost"],
        "policy": final_policy,
        "field_margin": field_margin,
        "ambiguity_status": ambiguity_status,
        "fields": results,
    }