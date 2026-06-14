import os
from pathlib import Path

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

    policy = event.get("input_policy", {})
    metadata = policy.get("metadata", {})
    measurements = get_event_measurements_for_policy(event)

    decision = policy.get("decision") or event.get("action") or "UNKNOWN"

    summary = (
        "ACA Runtime applied Input Policy Overlay before state mutation."
    )

    if decision == "DEFER_ORIGIN_LOW_SIGNAL":
        summary = (
            "The submitted text is low-signal. It may pass the application layer, "
            "but it is not admitted as semantic origin and does not mutate runtime state."
        )
    elif decision == "BOUNDARY_SECRET_REQUEST":
        summary = (
            "The submitted text triggered a credential boundary before trajectory contamination."
        )
    elif decision == "BOUNDARY_MANIPULATION_REQUEST":
        summary = (
            "The submitted text triggered a manipulation boundary before trajectory contamination."
        )
    elif decision == "SAFE_CREDENTIAL_GUIDANCE":
        summary = (
            "The submitted text is credential-related but defensive or recovery-oriented. "
            "Safe guidance is allowed without mutating runtime state."
        )
    elif decision == "ORIGIN_CANDIDATE":
        summary = (
            "The submitted text was admitted as a semantic origin candidate. "
            "Runtime state mutation is allowed."
        )

    fields = measurements.get("fields") or {}

    result = {
        "decision": decision,
        "semantic_field": metadata.get("F") or metadata.get("foundation") or "unknown",
        "secondary_field": metadata.get("C") or metadata.get("context") or "unknown",
        "criterion_confidence": (
            1.0 - float(metadata.get("foundation_cost", 1.0))
            if metadata.get("foundation_cost") is not None
            else None
        ),
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

    return {
        "summary": summary,
        "method": "measure_only + Input Policy Overlay + ACA artifact projection",
        "llm_generation_used": False,
        "result": result,
        "input_policy": policy,
        "application_response": event.get("application_response"),
        "raw_report": {
            "event": event,
            "raw_result": {
                "fields": fields,
                "measurements": measurements,
            },
        },
        "explanation": explanation,
    }
