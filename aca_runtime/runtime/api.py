from .loader import load_artifacts_atlas
from .runtime_report import build_runtime_report
from .text_evaluator import evaluate_text


def evaluate_runtime(text: str, artifacts_path: str) -> dict:
    atlas = load_artifacts_atlas(artifacts_path)
    result = evaluate_text(text, atlas)
    report = build_runtime_report(result)

    return {
        "report": report,
        "raw_result": result,
    }