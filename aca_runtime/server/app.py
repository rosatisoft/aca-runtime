from fastapi import FastAPI
from pydantic import BaseModel

from aca_runtime.runtime import (
    evaluate_runtime,
    evaluate_runtime_trajectory,
    evaluate_criterion_route,
)


DEFAULT_ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"

app = FastAPI(
    title="ACA Runtime Server",
    version="0.1.0",
    description="Geometry-based semantic criterion supervision runtime.",
)


class EvaluateRequest(BaseModel):
    text: str
    artifacts_path: str | None = None


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