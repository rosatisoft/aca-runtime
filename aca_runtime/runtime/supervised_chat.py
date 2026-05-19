from .api import (
    evaluate_runtime,
    evaluate_runtime_trajectory,
)

from .criterion_response import build_criterion_response


class SupervisedChat:

    def __init__(
        self,
        artifacts_path: str,
        drift_threshold: float = 0.20,
    ):
        self.artifacts_path = artifacts_path
        self.drift_threshold = drift_threshold
        self.history = []

    def _build_response(
        self,
        user_message,
        report,
        trajectory,
    ):
        criterion_response = build_criterion_response(
            user_message=user_message,
            runtime_report=report,
            trajectory_report=trajectory,
        )

        return criterion_response

    def step(
        self,
        user_message: str,
    ):

        self.history.append(user_message)

        runtime = evaluate_runtime(
            text=user_message,
            artifacts_path=self.artifacts_path,
        )

        trajectory = evaluate_runtime_trajectory(
            texts=self.history,
            artifacts_path=self.artifacts_path,
            drift_threshold=self.drift_threshold,
        )

        response = self._build_response(
            user_message,
            runtime["report"],
            trajectory["report"],
        )

        return {
            "user": user_message,
            "runtime": runtime["report"],
            "trajectory": trajectory["report"],
            "assistant": response,
        }