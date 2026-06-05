from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Protocol


@dataclass
class LLMResponse:
    provider: str
    model: str
    prompt: str
    response: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BaseLLMProvider(Protocol):
    provider_name: str
    model: str

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        ...