CRITERION_PREAMBLE = """
You will receive a criterion signal before each turn.

Use it to guide behavior, not as content to explain.
Do not classify the user's message as your final answer.

Preserve the active research objective unless the user explicitly declares a new frame.
"""


POLICY = {
    "ALLOW": {
        "meaning": "The current turn appears aligned with the active criterion.",
        "behavior": "Continue normally.",
    },

    "CLARIFY": {
        "meaning": "The current turn is ambiguous and may need a clearer frame.",
        "behavior": "Ask one concise clarification question before extending the analysis.",
    },

    "REANCHOR": {
        "meaning": "The current turn may pull the task away from the active evidence-based research criterion.",
        "behavior": "Continue the task, but keep the original research objective active.",
    },

    "DECLARED_SHIFT": {
        "meaning": "The user explicitly declared a new frame.",
        "behavior": "Acknowledge the declared frame briefly and continue under it.",
    },

    "RECOVERING": {
        "meaning": "The user declared a return toward a previous criterion, but stability is not fully restored yet.",
        "behavior": "Resume the previous objective cautiously and keep conclusions supported.",
    },
}


def build_criterion_action(
    runtime,
    trajectory,
    declared_shift=None,
):
    declared_shift = declared_shift or {}
    decision = runtime["decision"]

    is_declared = declared_shift.get("declared_shift", False)
    is_drifting = trajectory["drift_detected"]

    if is_declared and is_drifting:
        mode = "RECOVERING"
    elif is_declared:
        mode = "DECLARED_SHIFT"
    elif is_drifting or "DRIFT" in decision:
        mode = "REANCHOR"
    elif "CLARIFY" in decision:
        mode = "CLARIFY"
    else:
        mode = "ALLOW"

    return {
        "mode": mode,
        "meaning": POLICY[mode]["meaning"],
        "behavior": POLICY[mode]["behavior"],
    }


def build_minimal_prompt(
    criterion,
    objective=None,
):

    objective = (
        objective
        or
        "Continue the active task."
    )

    return f"""
{CRITERION_PREAMBLE}

Active Objective:
{objective}

Criterion Signal:
{criterion["mode"]}

Meaning:
{criterion["meaning"]}

Behavior:
{criterion["behavior"]}
"""