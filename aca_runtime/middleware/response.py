from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MiddlewareResponse:
    """
    Unified response object for ACA Runtime Middleware.

    This object is intentionally application-neutral. Applications may use
    the runtime_result, application_response, and post_generation_review fields
    to decide whether to answer, clarify, block, re-anchor, or display a report.
    """

    mode: str
    input_text: str
    objective: Optional[str]
    admitted: bool
    action: str
    final_response: Optional[str]
    llm_called: bool
    should_call_llm: bool
    boundary_applied: bool
    runtime_result: Optional[Dict[str, Any]] = None
    measurements: Optional[Dict[str, Any]] = None
    application_response: Optional[Dict[str, Any]] = None
    llm_response: Optional[Dict[str, Any]] = None
    post_generation_review: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
