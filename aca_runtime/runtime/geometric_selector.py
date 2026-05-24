from .api import evaluate_runtime
from .text_evaluator import embed_text
from .foundation_orientation import evaluate_foundation_orientation


OBJECTIVE_KEYWORDS = [
    "evidence",
    "study",
    "studies",
    "research",
    "measurable",
    "productivity",
    "remote work",
    "supported",
    "context",
]


def objective_alignment_score(
    candidate: str,
    objective: str | None = None,
) -> float:
    if not objective:
        return 0.0

    text = candidate.lower()
    objective_text = objective.lower()

    score = 0.0

    for word in OBJECTIVE_KEYWORDS:
        if word in text and word in objective_text:
            score += 0.15
        elif word in text:
            score += 0.08

    return min(score, 0.60)


def foundation_delta_score(
    candidate_orientation: float,
    objective_orientation: float,
) -> float:

    delta = (
        candidate_orientation
        - objective_orientation
    )

    return delta


def score_candidate(
    report: dict,
    candidate: str,
    objective: str | None = None,
    foundation_orientation: float = 0.0,
) -> float:
    origin_cost = report["origin_cost"]
    confidence = report["criterion_confidence"]
    decision = report["decision"]
    ambiguity = report["ambiguity"]

    drift_penalty = 0.40 if "DRIFT" in decision else 0.0
    clarify_penalty = 0.15 if "CLARIFY" in decision else 0.0
    ambiguity_penalty = 0.10 if ambiguity == "AMBIGUOUS" else 0.0

    objective_bonus = objective_alignment_score(
        candidate=candidate,
        objective=objective,
    )

    return (
        confidence
        - origin_cost
        - drift_penalty
        - clarify_penalty
        - ambiguity_penalty
        + objective_bonus
        + foundation_orientation
    )


def evaluate_candidate(
    candidate: str,
    artifacts_path: str,
    objective: str | None = None,
) -> dict:
    result = evaluate_runtime(
        text=candidate,
        artifacts_path=artifacts_path,
    )

    report = result["report"]

    candidate_vector = (
        embed_text(
            candidate
        )
    )

    candidate_foundation = (
        evaluate_foundation_orientation(
            vector=candidate_vector,
            artifacts_path=artifacts_path,
        )
    )

    candidate_orientation = (
        candidate_foundation[
            "foundation_orientation"
        ]
    )

    objective_orientation = 0.0

    if objective:

        objective_vector = (
            embed_text(
                objective
            )
        )

        objective_foundation = (
            evaluate_foundation_orientation(
                vector=objective_vector,
                artifacts_path=artifacts_path,
            )
        )

        objective_orientation = (
            objective_foundation[
                "foundation_orientation"
            ]
        )

    foundation_delta = (
        foundation_delta_score(
            candidate_orientation,
            objective_orientation,
        )
    )

    foundation_preserved = (
        foundation_delta
        >= -0.02
    )

    score = score_candidate(
        report=report,
        candidate=candidate,
        objective=objective,
        foundation_orientation=foundation_delta,
    )

    return {
        "candidate": candidate,
        "score": score,
        "objective_bonus": objective_alignment_score(
            candidate=candidate,
            objective=objective,
        ),
        "report": report,
        "candidate_orientation": candidate_orientation,
        "objective_orientation": objective_orientation,
        "foundation_delta": foundation_delta,
        "foundation_preserved": foundation_preserved,

        "orientation_diagnostic": {
            "candidate_orientation": candidate_orientation,
            "objective_orientation": objective_orientation,
            "foundation_delta": foundation_delta,
            "interpretation": (
                "diagnostic_only"
            ),
        },
     }


def select_best_candidate(
    candidates: list[str],
    artifacts_path: str,
    objective: str | None = None,
) -> dict:
    evaluated = [
        evaluate_candidate(
            candidate=candidate,
            artifacts_path=artifacts_path,
            objective=objective,
        )
        for candidate in candidates
    ]

    ranked = sorted(
        evaluated,
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "objective": objective,
        "selected": ranked[0],
        "ranked": ranked,
    }