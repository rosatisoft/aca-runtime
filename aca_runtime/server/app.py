import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from aca_runtime.runtime import (
    evaluate_runtime,
    evaluate_runtime_trajectory,
    evaluate_criterion_route,
)

from aca_runtime.middleware import ACAMiddleware
from aca_runtime.middleware_policy import (
    get_event_measurements_for_policy,
    handle_with_input_policy,
)


DEFAULT_ARTIFACTS_PATH = os.environ.get(
    "ACA_ARTIFACTS_PATH",
    str(Path.cwd() / "artifacts"),
)

POLICY_EVALUATE_METHOD = (
    "measure_only + Input Policy Overlay + ACA artifact projection"
)


DECISION_PRESENTATION: Dict[str, Dict[str, str]] = {
    "DEFER_ORIGIN_LOW_SIGNAL": {
        "category": "pass_through_no_origin",
        "status": "not_admitted",
        "severity": "low",
        "summary": (
            "The submitted text is low-signal. It may pass the application layer, "
            "but it is not admitted as semantic origin and does not mutate runtime state."
        ),
    },
    "ORIGIN_CANDIDATE": {
        "category": "origin_candidate",
        "status": "admitted",
        "severity": "normal",
        "summary": (
            "The submitted text was admitted as a semantic origin candidate. "
            "Runtime state mutation is allowed."
        ),
    },
    "BOUNDARY_SECRET_REQUEST": {
        "category": "credential_boundary",
        "status": "blocked",
        "severity": "high",
        "summary": (
            "The submitted text triggered a credential boundary before trajectory contamination."
        ),
    },
    "BOUNDARY_MANIPULATION_REQUEST": {
        "category": "manipulation_boundary",
        "status": "blocked",
        "severity": "high",
        "summary": (
            "The submitted text triggered a manipulation boundary before trajectory contamination."
        ),
    },
    "SAFE_CREDENTIAL_GUIDANCE": {
        "category": "safe_credential_guidance",
        "status": "safe_guidance",
        "severity": "medium",
        "summary": (
            "The submitted text is credential-related but defensive or recovery-oriented. "
            "Safe guidance is allowed without mutating runtime state."
        ),
    },
    "ASK_CLARIFICATION_SENSITIVE": {
        "category": "sensitive_clarification",
        "status": "clarify",
        "severity": "medium",
        "summary": (
            "The submitted text contains a sensitive credential-related signal with ambiguous intent."
        ),
    },
    "MONITOR_OR_ASK_CLARIFICATION": {
        "category": "monitor_or_clarify",
        "status": "monitor",
        "severity": "medium",
        "summary": (
            "The submitted text was not admitted as origin. Monitor or ask clarification before continuing."
        ),
    },
}


app = FastAPI(
    title="ACA Runtime Server",
    version="0.1.0",
    description="Geometry-based semantic criterion supervision runtime.",
)


class EvaluateRequest(BaseModel):
    text: str
    artifacts_path: str | None = None


class PolicyEvaluateRequest(BaseModel):
    text: str
    objective: str | None = "Analyze claims using only available evidence."
    artifacts_path: str | None = None
    mode: str = "supervise_only"


class TrajectoryRequest(BaseModel):
    texts: list[str]
    artifacts_path: str | None = None
    drift_threshold: float = 0.20


class CriterionRouteRequest(BaseModel):
    texts: list[str]
    artifacts_path: str | None = None
    drift_threshold: float = 0.20


def classify_decision(decision: str) -> Dict[str, str]:
    """Return the application-facing category/status/severity for a policy decision.

    This keeps decision presentation inside ACA Runtime so external orchestrators
    such as n8n do not duplicate policy interpretation logic.
    """

    return DECISION_PRESENTATION.get(
        decision,
        {
            "category": "unknown",
            "status": "review",
            "severity": "medium",
            "summary": "ACA Runtime applied Input Policy Overlay before state mutation.",
        },
    )


def build_policy_evaluate_response(
    *,
    event: Dict[str, Any],
    measurements: Dict[str, Any],
) -> Dict[str, Any]:
    """Build an application-ready /policy-evaluate response envelope.

    The envelope is intentionally flat at the top level for direct web/n8n use,
    while still preserving the detailed runtime objects for auditability and
    backwards compatibility.
    """

    policy = event.get("input_policy", {}) or {}
    app_response = event.get("application_response", {}) or {}
    metadata = policy.get("metadata", {}) or {}

    decision = policy.get("decision") or event.get("action") or "UNKNOWN"
    presentation = classify_decision(decision)
    fields = measurements.get("fields") or {}

    foundation_cost = metadata.get("foundation_cost")
    criterion_confidence = (
        1.0 - float(foundation_cost)
        if foundation_cost is not None
        else None
    )

    result = {
        "decision": decision,
        "semantic_field": metadata.get("F") or metadata.get("foundation") or "unknown",
        "secondary_field": metadata.get("C") or metadata.get("context") or "unknown",
        "criterion_confidence": criterion_confidence,
        "trajectory_state": (
            "state_mutation_allowed"
            if policy.get("state_mutation_allowed")
            else "no_state_mutation"
        ),
        "ambiguity": (
            "BOUNDARY"
            if policy.get("boundary_applied")
            else "ADMITTED"
            if policy.get("origin_allowed")
            else "NOT_ADMITTED"
        ),
    }

    explanation = [
        f"Input Policy decision: {decision}.",
        policy.get("reason", "No reason provided."),
        f"Origin allowed: {policy.get('origin_allowed')}.",
        f"State mutation allowed: {policy.get('state_mutation_allowed')}.",
        f"Boundary applied: {policy.get('boundary_applied')}.",
    ]

    message = (
        app_response.get("message")
        or policy.get("response_envelope")
        or policy.get("reason")
        or presentation["summary"]
    )

    return {
        "ok": True,
        "source": "ACA Runtime /policy-evaluate",
        "method": POLICY_EVALUATE_METHOD,
        "llm_generation_used": False,

        # Application-ready envelope.
        "decision": decision,
        "category": presentation["category"],
        "status": presentation["status"],
        "severity": presentation["severity"],
        "message": message,
        "summary": presentation["summary"],
        "should_call_llm": bool(app_response.get("should_call_llm", False)),
        "boundary_applied": bool(
            policy.get("boundary_applied") or app_response.get("boundary_applied")
        ),
        "origin_allowed": bool(policy.get("origin_allowed", False)),
        "state_mutation_allowed": bool(policy.get("state_mutation_allowed", False)),
        "semantic_field": result["semantic_field"],
        "context_field": metadata.get("C") or metadata.get("context"),
        "principle_field": metadata.get("P") or metadata.get("principle"),
        "transversal_field": metadata.get("T") or metadata.get("transversal"),
        "criterion_confidence": criterion_confidence,
        "trajectory_state": result["trajectory_state"],
        "ambiguity": result["ambiguity"],
        "metadata": metadata,
        "explanation": explanation,

        # Backwards-compatible detailed payload.
        "result": result,
        "input_policy": policy,
        "application_response": app_response,
        "raw_report": {
            "event": event,
            "raw_result": {
                "fields": fields,
                "measurements": measurements,
            },
        },
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "aca-runtime",
        "version": "0.1.0",
    }


@app.post("/evaluate")
def evaluate(request: EvaluateRequest):
    artifacts_path = request.artifacts_path or DEFAULT_ARTIFACTS_PATH

    return evaluate_runtime(
        text=request.text,
        artifacts_path=artifacts_path,
    )


@app.post("/trajectory")
def trajectory(request: TrajectoryRequest):
    artifacts_path = request.artifacts_path or DEFAULT_ARTIFACTS_PATH

    return evaluate_runtime_trajectory(
        texts=request.texts,
        artifacts_path=artifacts_path,
        drift_threshold=request.drift_threshold,
    )


@app.post("/criterion-route")
def criterion_route(request: CriterionRouteRequest):
    artifacts_path = request.artifacts_path or DEFAULT_ARTIFACTS_PATH

    return evaluate_criterion_route(
        texts=request.texts,
        artifacts_path=artifacts_path,
        drift_threshold=request.drift_threshold,
    )


@app.post("/policy-evaluate")
def policy_evaluate(request: PolicyEvaluateRequest):
    artifacts_path = request.artifacts_path or DEFAULT_ARTIFACTS_PATH

    middleware = ACAMiddleware(
        artifacts_root=artifacts_path,
        mode=request.mode,
        llm_provider=None,
    )

    event = handle_with_input_policy(
        middleware=middleware,
        text=request.text,
        objective=request.objective,
        mode=request.mode,
    )

    measurements = get_event_measurements_for_policy(event)

    return build_policy_evaluate_response(
        event=event,
        measurements=measurements,
    )
