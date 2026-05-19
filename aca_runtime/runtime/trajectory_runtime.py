import numpy as np

from .loader import load_artifacts_atlas
from .text_evaluator import evaluate_text


def compute_transition_score(cost_a: float, cost_b: float) -> float:
    """
    Difference between consecutive origin costs.
    """

    return abs(cost_b - cost_a)


def compute_trajectory_entropy(costs: list[float]) -> float:
    """
    Simple entropy proxy using variance.
    """

    if len(costs) < 2:
        return 0.0

    return float(np.var(costs))


def compute_preservation(costs: list[float]) -> float:
    """
    Preservation score:
    lower average cost -> stronger preservation.
    """

    mean_cost = np.mean(costs)

    preservation = 1.0 - mean_cost

    preservation = max(0.0, min(1.0, preservation))

    return float(preservation)


def evaluate_trajectory(
    texts: list[str],
    artifacts_path: str,
    drift_threshold: float = 0.15,
) -> dict:

    atlas = load_artifacts_atlas(artifacts_path)

    evaluations = []

    field_sequence = []

    origin_costs = []

    drift_events = []

    previous_cost = None

    previous_field = None

    for idx, text in enumerate(texts):

        result = evaluate_text(text, atlas)

        evaluations.append(result)

        best_field = result["best_field"]

        cost = result["origin_cost"]

        field_sequence.append(best_field)

        origin_costs.append(cost)

        if previous_cost is not None:

            transition = compute_transition_score(
                previous_cost,
                cost,
            )

            field_changed = previous_field != best_field

            if transition > drift_threshold or field_changed:

                drift_events.append({
                    "step": idx,
                    "transition_score": transition,
                    "field_changed": field_changed,
                    "from_field": previous_field,
                    "to_field": best_field,
                })

        previous_cost = cost

        previous_field = best_field

    entropy = compute_trajectory_entropy(origin_costs)

    preservation = compute_preservation(origin_costs)

    trajectory_status = "stable"

    if entropy > 0.10:
        trajectory_status = "unstable"

    if drift_events:
        trajectory_status = "drifting"

    return {
        "trajectory_status": trajectory_status,
        "drift_detected": len(drift_events) > 0,
        "field_sequence": field_sequence,
        "origin_costs": origin_costs,
        "criterion_preservation": preservation,
        "trajectory_entropy": entropy,
        "drift_events": drift_events,
        "evaluations": evaluations,
    }