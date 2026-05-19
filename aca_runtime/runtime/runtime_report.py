def compute_confidence(origin_cost: float) -> float:
    """
    Simple inverse confidence model.
    Lower origin cost -> higher confidence.
    """

    confidence = 1.0 - origin_cost

    confidence = max(0.0, min(1.0, confidence))

    return confidence


def determine_runtime_status(policy: str) -> str:
    if policy == "ALLOW":
        return "stable"

    if policy == "ALLOW_LIGHT":
        return "light_monitoring"

    if policy in ["CLARIFY", "AMBIGUOUS_CLARIFY"]:
        return "clarification_required"

    if policy in ["FLAG_DRIFT", "AMBIGUOUS_DRIFT"]:
        return "semantic_drift"

    return "unknown"


def determine_trajectory_state(
    ambiguity_status: str,
    origin_cost: float,
) -> str:

    if origin_cost < 0.25 and ambiguity_status == "CLEAR":
        return "stable_alignment"

    if ambiguity_status == "AMBIGUOUS":
        return "unstable_transition"

    if origin_cost > 0.75:
        return "high_entropy"

    return "moderate_variation"


def build_runtime_report(result: dict) -> dict:

    confidence = compute_confidence(
        result["origin_cost"]
    )

    runtime_status = determine_runtime_status(
        result["policy"]
    )

    trajectory_state = determine_trajectory_state(
        result["ambiguity_status"],
        result["origin_cost"],
    )

    return {
        "runtime_status": runtime_status,
        "decision": result["policy"],
        "semantic_field": result["best_field"],
        "secondary_field": result["second_best_field"],
        "origin_cost": result["origin_cost"],
        "field_margin": result["field_margin"],
        "ambiguity": result["ambiguity_status"],
        "criterion_confidence": confidence,
        "trajectory_state": trajectory_state,
    }