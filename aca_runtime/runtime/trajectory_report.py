def determine_drift_severity(drift_events: list[dict]) -> str:
    if not drift_events:
        return "none"

    max_transition = max(
        event["transition_score"]
        for event in drift_events
    )

    if max_transition >= 0.50:
        return "high"

    if max_transition >= 0.25:
        return "moderate"

    return "low"


def build_trajectory_report(result: dict) -> dict:
    drift_severity = determine_drift_severity(
        result["drift_events"]
    )

    return {
        "trajectory_status": result["trajectory_status"],
        "drift_detected": result["drift_detected"],
        "drift_severity": drift_severity,
        "field_sequence": result["field_sequence"],
        "criterion_preservation": result["criterion_preservation"],
        "trajectory_entropy": result["trajectory_entropy"],
        "drift_event_count": len(result["drift_events"]),
        "drift_events": result["drift_events"],
    }