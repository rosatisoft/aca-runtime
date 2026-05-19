def summarize_runtime_signal(runtime_report: dict) -> str:
    decision = runtime_report["decision"]
    field = runtime_report["semantic_field"]
    secondary = runtime_report["secondary_field"]
    cost = runtime_report["origin_cost"]
    ambiguity = runtime_report["ambiguity"]

    return (
        f"Decision={decision}; "
        f"Field={field}; "
        f"Secondary={secondary}; "
        f"OriginCost={cost:.4f}; "
        f"Ambiguity={ambiguity}"
    )


def summarize_trajectory_signal(trajectory_report: dict) -> str:
    status = trajectory_report["trajectory_status"]
    drift = trajectory_report["drift_detected"]
    severity = trajectory_report["drift_severity"]
    preservation = trajectory_report["criterion_preservation"]

    return (
        f"TrajectoryStatus={status}; "
        f"DriftDetected={drift}; "
        f"Severity={severity}; "
        f"Preservation={preservation:.4f}"
    )


def build_clarification_question(runtime_report: dict, trajectory_report: dict) -> str:
    field = runtime_report["semantic_field"]
    decision = runtime_report["decision"]

    if "DRIFT" in decision:
        return (
            "Your message appears to move away from the current criterion trajectory. "
            "Should I treat this as a hypothetical, a factual claim, or a rhetorical example?"
        )

    if "CLARIFY" in decision:
        return (
            f"Your message is closest to the {field} field, but the criterion signal is not stable enough. "
            "Could you clarify what standard of evidence or interpretation should guide the answer?"
        )

    if decision == "ALLOW_LIGHT":
        return (
            "There is mild ambiguity in the current message. "
            "Should I proceed with the most coherent interpretation, or would you like to narrow the context?"
        )

    return (
        "The current message appears stable. "
        "I can proceed while preserving the detected criterion orientation."
    )


def build_response_guidance(runtime_report: dict, trajectory_report: dict) -> list[str]:
    guidance = []

    decision = runtime_report["decision"]
    field = runtime_report["semantic_field"]

    if field == "factual":
        guidance.append(
            "Separate factual claims from speculation and avoid asserting unsupported facts."
        )

    if field == "foundational":
        guidance.append(
            "Preserve logical coherence, identity, non-contradiction, and continuity of interpretation."
        )

    if field == "rhetorical":
        guidance.append(
            "Identify persuasive or rhetorical framing before drawing conclusions."
        )

    if runtime_report["ambiguity"] == "AMBIGUOUS":
        guidance.append(
            "Avoid overconfident conclusions because the field margin is narrow."
        )

    if trajectory_report["drift_detected"]:
        guidance.append(
            "Account for semantic drift across the conversation before answering."
        )

    if "DRIFT" in decision:
        guidance.append(
            "Do not continue as if the prior criterion remains stable; request clarification or re-anchor the discussion."
        )

    if not guidance:
        guidance.append(
            "Proceed normally while preserving the current semantic orientation."
        )

    return guidance


def build_criterion_response(
    user_message: str,
    runtime_report: dict,
    trajectory_report: dict,
) -> dict:
    signal_summary = summarize_runtime_signal(runtime_report)
    trajectory_summary = summarize_trajectory_signal(trajectory_report)

    clarification_question = build_clarification_question(
        runtime_report=runtime_report,
        trajectory_report=trajectory_report,
    )

    response_guidance = build_response_guidance(
        runtime_report=runtime_report,
        trajectory_report=trajectory_report,
    )

    assistant_message=clarification_question

    return {
        "user_message": user_message,
        "assistant_message": assistant_message,
        "signal_summary": signal_summary,
        "trajectory_summary": trajectory_summary,
        "recommended_action": runtime_report["decision"],
        "clarification_question": clarification_question,
        "response_guidance": response_guidance,
    }