from .criterion_response import build_criterion_response
from .api import evaluate_runtime, evaluate_runtime_trajectory
from .declared_shift import detect_declared_shift


VALID_MODES = [
    "report",
    "warning",
    "interactive",
    "moderator",
]


def supervise_message(
    user_message: str,
    history: list[str],
    artifacts_path: str,
    mode: str = "report",
    drift_threshold: float = 0.20,
) -> dict:
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid supervision mode: {mode}")

    updated_history = history + [user_message]

    runtime = evaluate_runtime(
        text=user_message,
        artifacts_path=artifacts_path,
    )

    trajectory = evaluate_runtime_trajectory(
        texts=updated_history,
        artifacts_path=artifacts_path,
        drift_threshold=drift_threshold,
    )


    declared_shift = detect_declared_shift(user_message)

    criterion_response = build_criterion_response(
        user_message=user_message,
        runtime_report=runtime["report"],
        trajectory_report=trajectory["report"],
    )

    intervention = build_mode_intervention(
        mode=mode,
        runtime_report=runtime["report"],
        trajectory_report=trajectory["report"],
        criterion_response=criterion_response,
    )

    return {
        "mode": mode,
        "user_message": user_message,
        "history": updated_history,
        "runtime": runtime["report"],
        "trajectory": trajectory["report"],
        "criterion_response": criterion_response,
        "declared_shift": declared_shift,
        "intervention": intervention,
    }


def build_mode_intervention(
    mode: str,
    runtime_report: dict,
    trajectory_report: dict,
    criterion_response: dict,
) -> dict:
    decision = runtime_report["decision"]
    drift_detected = trajectory_report["drift_detected"]

    if mode == "report":
        return {
            "should_intervene": False,
            "level": "silent",
            "message": "ACA is reporting only.",
            "action": "observe",
        }

    if mode == "warning":
        if drift_detected or "DRIFT" in decision or "CLARIFY" in decision:
            return {
                "should_intervene": True,
                "level": "warning",
                "message": criterion_response["assistant_message"],
                "action": "warn",
            }

        return {
            "should_intervene": False,
            "level": "stable",
            "message": "No warning required.",
            "action": "allow",
        }

    if mode == "interactive":
        if "DRIFT" in decision or "CLARIFY" in decision:
            return {
                "should_intervene": True,
                "level": "blocking",
                "message": criterion_response["assistant_message"],
                "action": "clarify_before_answering",
            }

        return {
            "should_intervene": False,
            "level": "stable",
            "message": "Proceed with response.",
            "action": "allow",
        }

    if mode == "moderator":
        if drift_detected or "DRIFT" in decision:
            return {
                "should_intervene": True,
                "level": "moderator_alert",
                "message": (
                    "Moderator notice: a criterion drift or undeclared semantic shift "
                    "was detected. Participants should clarify whether the current "
                    "claim is factual, hypothetical, rhetorical, or evidential."
                ),
                "action": "moderate",
            }

        if "CLARIFY" in decision:
            return {
                "should_intervene": True,
                "level": "moderator_note",
                "message": (
                    "Moderator note: the current contribution is ambiguous and should "
                    "be clarified before continuing."
                ),
                "action": "request_clarification",
            }

        return {
            "should_intervene": False,
            "level": "stable",
            "message": "Moderator notice: criterion remains stable.",
            "action": "allow",
        }

    return {
        "should_intervene": False,
        "level": "unknown",
        "message": "Unknown mode.",
        "action": "none",
    }