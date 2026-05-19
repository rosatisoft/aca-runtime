from .loader import load_artifacts_atlas
from .runtime_report import build_runtime_report
from .text_evaluator import evaluate_text
from .trajectory_report import build_trajectory_report
from .trajectory_runtime import evaluate_trajectory


def evaluate_runtime(text: str, artifacts_path: str) -> dict:
    atlas = load_artifacts_atlas(artifacts_path)
    result = evaluate_text(text, atlas)
    report = build_runtime_report(result)

    return {
        "report": report,
        "raw_result": result,
    }


def evaluate_runtime_trajectory(
    texts: list[str],
    artifacts_path: str,
    drift_threshold: float = 0.20,
) -> dict:
    result = evaluate_trajectory(
        texts=texts,
        artifacts_path=artifacts_path,
        drift_threshold=drift_threshold,
    )

    report = build_trajectory_report(result)

    return {
        "report": report,
        "raw_result": result,
    }