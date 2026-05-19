from .trajectory_report import build_trajectory_report
from .trajectory_runtime import evaluate_trajectory


def classify_section_risk(evaluation: dict) -> str:
    policy = evaluation["policy"]
    ambiguity = evaluation["ambiguity_status"]
    origin_cost = evaluation["origin_cost"]

    if policy in ["FLAG_DRIFT", "AMBIGUOUS_DRIFT"]:
        return "high"

    if policy in ["CLARIFY", "AMBIGUOUS_CLARIFY"]:
        return "moderate"

    if ambiguity == "AMBIGUOUS" or origin_cost > 0.45:
        return "moderate"

    return "low"


def build_section_annotations(texts: list[str], evaluations: list[dict]) -> list[dict]:
    annotations = []

    for idx, evaluation in enumerate(evaluations):
        annotations.append({
            "section": idx,
            "text": texts[idx],
            "best_field": evaluation["best_field"],
            "second_best_field": evaluation["second_best_field"],
            "origin_cost": evaluation["origin_cost"],
            "field_margin": evaluation["field_margin"],
            "ambiguity": evaluation["ambiguity_status"],
            "policy": evaluation["policy"],
            "risk": classify_section_risk(evaluation),
        })

    return annotations


def build_reasoning_guidance(
    trajectory_report: dict,
    section_annotations: list[dict],
) -> list[str]:
    guidance = []

    if trajectory_report["drift_detected"]:
        guidance.append(
            "Review the sections where semantic drift was detected before producing a final answer."
        )

    if trajectory_report["drift_severity"] == "high":
        guidance.append(
            "Treat high-severity field transitions as potential changes in meaning, framing, or epistemic orientation."
        )

    ambiguous_sections = [
        s["section"]
        for s in section_annotations
        if s["ambiguity"] == "AMBIGUOUS"
    ]

    if ambiguous_sections:
        guidance.append(
            f"Sections {ambiguous_sections} are semantically ambiguous; avoid overconfident conclusions from them."
        )

    high_risk_sections = [
        s["section"]
        for s in section_annotations
        if s["risk"] == "high"
    ]

    if high_risk_sections:
        guidance.append(
            f"Sections {high_risk_sections} are high-risk; separate factual claims from rhetoric or unsupported assertions."
        )

    if not guidance:
        guidance.append(
            "The trajectory appears stable; reason normally while preserving the detected semantic field orientation."
        )

    return guidance


def build_criterion_route(
    texts: list[str],
    artifacts_path: str,
    drift_threshold: float = 0.20,
) -> dict:
    trajectory_result = evaluate_trajectory(
        texts=texts,
        artifacts_path=artifacts_path,
        drift_threshold=drift_threshold,
    )

    trajectory_report = build_trajectory_report(trajectory_result)

    section_annotations = build_section_annotations(
        texts=texts,
        evaluations=trajectory_result["evaluations"],
    )

    guidance = build_reasoning_guidance(
        trajectory_report=trajectory_report,
        section_annotations=section_annotations,
    )

    return {
        "criterion_route": trajectory_report,
        "section_annotations": section_annotations,
        "llm_guidance": guidance,
    }