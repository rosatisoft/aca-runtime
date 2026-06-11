from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


def utc_now_iso() -> str:
    """Return a timezone-aware UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CriterionTrace:
    """
    Serializable record of a single ACA Runtime criterion decision.

    A CriterionTrace is not a prompt, not a policy, and not a model response.
    It is an auditable record of how ACA Runtime evaluated an input and how
    the application decided to act on that evaluation.

    The trace is intentionally JSONL-friendly so it can later become a dataset
    for calibration, benchmarking, auditing, and future model-side criterion
    training.
    """

    trace_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now_iso)

    source: str = "unknown"
    input_text: str = ""

    foundation: Optional[str] = None
    context: Optional[str] = None
    principle: Optional[str] = None
    semantic_field: Optional[str] = None

    origin_cost: Optional[float] = None
    decision: str = "MEASURE_ONLY"
    reason: Optional[str] = None

    trajectory_state: Optional[str] = None
    application_action: Optional[str] = None
    mutated_state: bool = False

    runtime_status: Optional[str] = None
    policy_state: Optional[str] = None
    confidence: Optional[float] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the trace to a plain dictionary."""
        return asdict(self)

    @classmethod
    def from_runtime_result(
        cls,
        *,
        input_text: str,
        runtime_result: Dict[str, Any],
        source: str = "unknown",
        application_action: Optional[str] = None,
        mutated_state: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "CriterionTrace":
        """
        Build a CriterionTrace from a runtime result dictionary.

        This method is intentionally tolerant: different ACA Runtime layers may
        return slightly different field names. The trace captures whatever is
        available without breaking the caller.
        """

        measurement = runtime_result.get("measurement", {}) or {}
        triaxial = runtime_result.get("triaxial", {}) or {}
        decision_block = runtime_result.get("decision", {}) or {}
        policy = runtime_result.get("policy", {}) or {}

        decision = (
            runtime_result.get("decision")
            if isinstance(runtime_result.get("decision"), str)
            else decision_block.get("action")
            or decision_block.get("decision")
            or runtime_result.get("action")
            or runtime_result.get("policy_decision")
            or "MEASURE_ONLY"
        )

        reason = (
            runtime_result.get("reason")
            or decision_block.get("reason")
            or policy.get("reason")
            or runtime_result.get("explanation")
        )

        return cls(
            source=source,
            input_text=input_text,
            foundation=(
                runtime_result.get("foundation")
                or triaxial.get("foundation")
                or measurement.get("foundation")
            ),
            context=(
                runtime_result.get("context")
                or triaxial.get("context")
                or measurement.get("context")
            ),
            principle=(
                runtime_result.get("principle")
                or triaxial.get("principle")
                or measurement.get("principle")
            ),
            semantic_field=(
                runtime_result.get("semantic_field")
                or runtime_result.get("field")
                or measurement.get("semantic_field")
                or measurement.get("field")
            ),
            origin_cost=(
                runtime_result.get("origin_cost")
                or measurement.get("origin_cost")
            ),
            decision=str(decision),
            reason=reason,
            trajectory_state=(
                runtime_result.get("trajectory_state")
                or runtime_result.get("state")
                or measurement.get("trajectory_state")
            ),
            application_action=application_action,
            mutated_state=mutated_state,
            runtime_status=runtime_result.get("runtime_status"),
            policy_state=(
                runtime_result.get("policy_state")
                or policy.get("state")
                or policy.get("policy_state")
            ),
            confidence=(
                runtime_result.get("confidence")
                or measurement.get("confidence")
            ),
            metadata=metadata or {},
        )
