def build_criterion_action(
    runtime,
    trajectory,
    intervention,
):

    decision = runtime["decision"]

    if (
        intervention["action"]
        == "acknowledge_declared_transition"
    ):

        return {
            "mode": "DECLARED_SHIFT",
            "instruction": (
                "Acknowledge the declared frame and continue."
            ),
        }

    if trajectory["drift_detected"]:

        return {
            "mode": "MODERATOR_CHECK",
            "instruction": (
                "Before continuing, determine whether "
                "the current contribution should be "
                "treated as factual, hypothetical, "
                "rhetorical, or evidential."
            ),
        }

    if "CLARIFY" in decision:

        return {
            "mode": "CLARIFY",
            "instruction": (
                "Ask one clarification question "
                "before continuing."
            ),
        }

    return {
        "mode": "ALLOW",
        "instruction": (
            "Continue normally."
        ),
    }