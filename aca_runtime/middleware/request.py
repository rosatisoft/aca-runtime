from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Literal, Optional

MiddlewareMode = Literal[
    "measure_only",
    "supervise_only",
    "generate",
]


@dataclass
class MiddlewareRequest:
    """
    Request object for ACA Runtime Middleware.

    Modes:
    - measure_only: measure Atlas orientation without mutating runtime state.
    - supervise_only: run Runtime v2 precondition/state logic without calling an LLM.
    - generate: call an LLM provider only when Runtime permits generation, then review output.
    """

    text: str
    objective: Optional[str] = None
    mode: MiddlewareMode = "supervise_only"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
