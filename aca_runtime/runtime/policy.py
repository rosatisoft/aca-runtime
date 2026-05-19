def decide_policy(origin_cost: float, threshold: float) -> str:
    if origin_cost <= threshold:
        return "ALLOW"
    if origin_cost <= threshold * 1.5:
        return "CLARIFY"
    return "FLAG_DRIFT"