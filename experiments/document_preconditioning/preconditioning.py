def infer_state(section: dict) -> str:
    policy = section.get("policy")
    risk = section.get("risk")
    ambiguity = section.get("ambiguity")

    if policy in ["FLAG_DRIFT", "AMBIGUOUS_DRIFT"] or risk == "high":
        return "DRIFT"

    if policy in ["CLARIFY", "AMBIGUOUS_CLARIFY"] or ambiguity == "AMBIGUOUS":
        return "SHIFT_OR_AMBIGUITY"

    return "ALIGN"


def build_preconditioning_prompt(route):

    route_text = "\n".join(
        [
            (
                f"Section {r['section']}: "
                f"{infer_state(r)} "
                f"(field={r['best_field']}, risk={r['risk']})"
            )
            for r in route
        ]
    )

    return f"""
Analyze the document as a trajectory.

Observe:

ALIGN
SHIFT
DRIFT
CONTRADICTION
RECOVERY

Report only supported transitions.

Do not infer intention.

Criterion Route:

{route_text}
"""