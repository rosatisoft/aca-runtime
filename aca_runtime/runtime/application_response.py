from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class ApplicationResponse:
    response_type: str
    message: str
    should_call_llm: bool
    boundary_applied: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_application_response(
    runtime_result: Dict[str, Any],
) -> ApplicationResponse:
    """
    Builds a deterministic application-level response from ACA Runtime v2.

    This module does not measure, classify, or mutate state.
    It only translates Runtime state into a user-facing response.
    """

    precondition = runtime_result["precondition"]
    state = precondition["state"]
    action = runtime_result["action"]
    summary = runtime_result.get("measurements_summary", {})
    tags = precondition.get("tags", [])

    if state == "ACCEPT_AS_ORIGIN":
        return ApplicationResponse(
            response_type="origin_accepted",
            message=(
                "Input accepted as semantic origin. "
                "A new accepted trajectory has been established."
            ),
            should_call_llm=True,
            boundary_applied=False,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    if state == "ACCEPT_AS_CONTINUATION":
        return ApplicationResponse(
            response_type="continuation_accepted",
            message=(
                "Input accepted as trajectory continuation. "
                "The accepted semantic trajectory has been updated."
            ),
            should_call_llm=True,
            boundary_applied=False,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    if state == "ASK_CLARIFICATION":
        return ApplicationResponse(
            response_type="clarification_required",
            message=(
                "Please clarify the objective before continuing. "
                "This input is not specific enough to become semantic origin "
                "or modify the accepted trajectory."
            ),
            should_call_llm=False,
            boundary_applied=True,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    if state == "REJECT_PREDEFINED_RISK":
        return ApplicationResponse(
            response_type="predefined_risk_rejected",
            message=(
                "I cannot help request, obtain, reveal, or submit sensitive "
                "access information such as passwords, private keys, tokens, "
                "verification codes, or credentials."
            ),
            should_call_llm=False,
            boundary_applied=True,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    if state == "FLAG_OUT_OF_FIELD":
        return ApplicationResponse(
            response_type="out_of_field",
            message=(
                "I cannot establish a stable semantic origin from this input. "
                "Please restate it with a clear objective or meaningful context."
            ),
            should_call_llm=False,
            boundary_applied=True,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    if state == "BOUNDARY_RESPONSE":
        return ApplicationResponse(
            response_type="boundary_response",
            message=(
                "I can help with this in a protective way. "
                "Do not share passwords, private keys, tokens, verification codes, "
                "or credentials. Use official or independently verified channels "
                "and report suspicious requests."
            ),
            should_call_llm=False,
            boundary_applied=True,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    if state == "DECLARE_INTENT":
        return ApplicationResponse(
            response_type="intent_confirmation_required",
            message=(
                "This appears to involve a specific intent that should be confirmed "
                "before continuing. Please clarify the legitimate objective."
            ),
            should_call_llm=False,
            boundary_applied=True,
            metadata={
                "state": state,
                "action": action,
                "summary": summary,
                "tags": tags,
            },
        )

    return ApplicationResponse(
        response_type="monitoring",
        message="Runtime state recorded. Continue monitoring.",
        should_call_llm=False,
        boundary_applied=False,
        metadata={
            "state": state,
            "action": action,
            "summary": summary,
            "tags": tags,
        },
    )