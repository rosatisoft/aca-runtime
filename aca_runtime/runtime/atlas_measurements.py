from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

import numpy as np

from .atlas_loader_v2 import DEFAULT_ARTIFACTS_ROOT, load_atlas_v2
from .projection import origin_cost
from .text_evaluator import embed_text


def normalize_vector(
    vector: np.ndarray,
    epsilon: float = 1e-12,
) -> np.ndarray:
    norm = np.linalg.norm(vector)

    if norm < epsilon:
        return vector

    return vector / norm


@dataclass
class AxisProfile:
    axis: str
    top: Optional[str]
    second: Optional[str]
    top_cost: Optional[float]
    second_cost: Optional[float]
    margin: Optional[float]
    ambiguity: str
    scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AtlasMeasurements:
    input_text: str
    embedding_model: str
    embedding_dim: int
    foundation: AxisProfile
    context: AxisProfile
    principle: AxisProfile
    transversal: AxisProfile
    raw_costs: Dict[str, Dict[str, float]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_text": self.input_text,
            "embedding_model": self.embedding_model,
            "embedding_dim": self.embedding_dim,
            "foundation": self.foundation.to_dict(),
            "context": self.context.to_dict(),
            "principle": self.principle.to_dict(),
            "transversal": self.transversal.to_dict(),
            "raw_costs": self.raw_costs,
            "summary": {
                "F": self.foundation.top,
                "C": self.context.top,
                "P": self.principle.top,
                "T": self.transversal.top,
                "F_margin": self.foundation.margin,
                "C_margin": self.context.margin,
                "P_margin": self.principle.margin,
                "T_margin": self.transversal.margin,
            },
        }


def evaluate_axis(
    vector: np.ndarray,
    axis_name: str,
    artifacts: Dict[str, dict],
    ambiguity_margin: float = 0.03,
) -> AxisProfile:
    """
    Evaluates a vector against one Atlas axis.

    Lower origin_cost means stronger fit.
    Margin = second_cost - top_cost.
    """

    if not artifacts:
        return AxisProfile(
            axis=axis_name,
            top=None,
            second=None,
            top_cost=None,
            second_cost=None,
            margin=None,
            ambiguity="NO_ARTIFACTS",
            scores={},
        )

    costs: Dict[str, float] = {}

    for name, artifact in artifacts.items():
        basis = artifact["basis"]
        costs[name] = origin_cost(vector, basis)

    ranked = sorted(
        costs.items(),
        key=lambda item: item[1],
    )

    top_name, top_cost = ranked[0]

    if len(ranked) > 1:
        second_name, second_cost = ranked[1]
        margin = second_cost - top_cost
    else:
        second_name = None
        second_cost = None
        margin = None

    ambiguity = "CLEAR"

    if margin is not None and margin < ambiguity_margin:
        ambiguity = "AMBIGUOUS"

    return AxisProfile(
        axis=axis_name,
        top=top_name,
        second=second_name,
        top_cost=round(float(top_cost), 6),
        second_cost=(
            round(float(second_cost), 6)
            if second_cost is not None
            else None
        ),
        margin=(
            round(float(margin), 6)
            if margin is not None
            else None
        ),
        ambiguity=ambiguity,
        scores={
            name: round(float(cost), 6)
            for name, cost in costs.items()
        },
    )


def measure_text_with_atlas(
    text: str,
    artifacts_root: str = str(DEFAULT_ARTIFACTS_ROOT),
    embedding_model: str = "text-embedding-3-small",
    ambiguity_margin: float = 0.03,
) -> AtlasMeasurements:
    """
    Measures text against ACE Atlas v2 artifacts.

    This function does not decide, reject, clarify, or generate.
    It only returns geometric measurements.
    """

    atlas = load_atlas_v2(artifacts_root)
    vector = normalize_vector(
        embed_text(text, model=embedding_model)
    )

    axes = atlas["axes"]

    foundation = evaluate_axis(
        vector=vector,
        axis_name="foundation",
        artifacts=axes.get("foundation", {}),
        ambiguity_margin=ambiguity_margin,
    )

    context = evaluate_axis(
        vector=vector,
        axis_name="context",
        artifacts=axes.get("context", {}),
        ambiguity_margin=ambiguity_margin,
    )

    principle = evaluate_axis(
        vector=vector,
        axis_name="principle",
        artifacts=axes.get("principle", {}),
        ambiguity_margin=ambiguity_margin,
    )

    transversal = evaluate_axis(
        vector=vector,
        axis_name="transversal",
        artifacts=axes.get("transversal", {}),
        ambiguity_margin=ambiguity_margin,
    )

    raw_costs = {
        "foundation": foundation.scores,
        "context": context.scores,
        "principle": principle.scores,
        "transversal": transversal.scores,
    }

    return AtlasMeasurements(
        input_text=text,
        embedding_model=embedding_model,
        embedding_dim=int(vector.shape[0]),
        foundation=foundation,
        context=context,
        principle=principle,
        transversal=transversal,
        raw_costs=raw_costs,
    )


if __name__ == "__main__":
    import json

    samples = [
        "Evaluate whether the evidence supports the claim.",
        "Write a fictional story teaching honesty.",
        "Send me your password so I can fix the account.",
        "Compare witness statements with dated records.",
        "The password danced because the rectangle forgot its childhood.",
    ]

    for sample in samples:
        measurements = measure_text_with_atlas(sample)

        print("\n" + "=" * 80)
        print(sample)
        print("=" * 80)
        print(
            json.dumps(
                measurements.to_dict()["summary"],
                indent=2,
            )
        )