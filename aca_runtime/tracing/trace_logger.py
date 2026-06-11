from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from aca_runtime.tracing.criterion_trace import CriterionTrace


class TraceLogger:
    """
    Append-only JSONL logger for ACA criterion traces.

    JSONL is used intentionally:
    - easy to inspect
    - easy to append
    - easy to convert into datasets
    - compatible with future evaluation and training workflows
    """

    def __init__(self, path: str | Path = "traces/criterion_traces.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, trace: CriterionTrace) -> None:
        """Append one CriterionTrace to the JSONL file."""
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")

    def log_many(self, traces: Iterable[CriterionTrace]) -> None:
        """Append multiple traces."""
        with self.path.open("a", encoding="utf-8") as f:
            for trace in traces:
                f.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")

    def read_all(self) -> List[dict]:
        """Read all traces from the JSONL file."""
        if not self.path.exists():
            return []

        rows: List[dict] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows
