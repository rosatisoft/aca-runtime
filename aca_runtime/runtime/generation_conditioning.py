from __future__ import annotations

from typing import Any, Dict


def build_compact_orientation(runtime_result: Dict[str, Any]) -> str:
    """
    Builds compact internal ACA Runtime orientation for an LLM.

    This orientation is used silently by the model and should not be
    exposed in the user-facing answer.
    """

    summary = runtime_result.get("measurements_summary", {})
    snapshot = runtime_result.get("state_snapshot", {})
    precondition = runtime_result.get("precondition", {})
    app_response = runtime_result.get("application_response", {})

    origin = snapshot.get("origin_text")
    objective = snapshot.get("objective")

    return f"""Internal ACA Runtime orientation.
Use this orientation silently. Do not mention ACA Runtime, Atlas, F-C-P, triaxial orientation, margins, response type, or internal state in the user-facing answer.

Runtime state:
- Precondition: {precondition.get("state")}
- Application action: {runtime_result.get("action")}
- Response type: {app_response.get("response_type")}

Accepted origin:
{origin}

Active objective:
{objective}

Semantic orientation:
- Foundation: {summary.get("F")}
- Context: {summary.get("C")}
- Principle: {summary.get("P")}

Generation constraints:
- Preserve the accepted origin and active objective.
- Stay aligned with the semantic orientation.
- Do not introduce unsupported certainty.
- Do not shift context or principle without making the shift explicit.
- If the user asks to evaluate evidence but no evidence is provided, ask for the claim and evidence.
- If the user asks for comparison but the materials are not provided, ask for the materials.
- Answer clearly and concisely.
- Do not expose internal runtime terminology.
"""


def build_supervised_prompt(
    user_input: str,
    runtime_result: Dict[str, Any],
) -> str:
    orientation = build_compact_orientation(runtime_result)

    return f"""{orientation}

User input:
{user_input}

Response:
"""