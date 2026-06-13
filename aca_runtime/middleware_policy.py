from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Protocol

from aca_runtime.runtime.input_policy import interpret_input_policy


class MiddlewareLike(Protocol):
    def handle(
        self,
        text: str,
        objective: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> Any:
        ...


def get_nested(data: Mapping[str, Any], *path: str, default: Any = None) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, Mapping):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def get_event_measurements_for_policy(event: Mapping[str, Any]) -> Dict[str, Any]:
    if event.get("measurements"):
        return dict(event["measurements"])

    measurements = get_nested(
        event,
        "runtime_result",
        "precondition",
        "metadata",
        "measurements",
        default={},
    )

    return dict(measurements or {})


def attach_input_policy(event: Dict[str, Any], *, text: str) -> Dict[str, Any]:
    measurements = get_event_measurements_for_policy(event)

    if not text or not measurements:
        return event

    policy = interpret_input_policy(text=text, measurements=measurements)
    event["input_policy"] = policy.to_dict()
    return event


def handle_with_input_policy(
    middleware: MiddlewareLike,
    *,
    text: str,
    objective: Optional[str] = None,
    mode: str = "supervise_only",
) -> Dict[str, Any]:
    """Run ACA middleware with input-policy enforcement before state mutation.

    Flow:
    1. measure_only preflight without mutating runtime state;
    2. interpret Input Policy Overlay over Atlas measurements;
    3. call stateful middleware only when state_mutation_allowed=True.

    Low-signal inputs may pass the application layer without semantic admission.
    Sensitive inputs may receive a boundary or safe guidance without mutating
    origin or trajectory.
    """

    preflight_result = middleware.handle(
        text=text,
        objective=objective,
        mode="measure_only",
    )
    preflight_event = preflight_result.to_dict()

    measurements = get_event_measurements_for_policy(preflight_event)
    policy = interpret_input_policy(text=text, measurements=measurements)
    policy_dict = policy.to_dict()
    preflight_event["input_policy"] = policy_dict

    if mode == "measure_only":
        return preflight_event

    state_mutation_allowed = bool(policy_dict.get("state_mutation_allowed", False))
    boundary_applied = bool(policy_dict.get("boundary_applied", False))

    if state_mutation_allowed and not boundary_applied:
        result = middleware.handle(
            text=text,
            objective=objective,
            mode=mode,
        )
        event = result.to_dict()
        event["input_policy"] = policy_dict
        return event

    message = (
        policy_dict.get("response_envelope")
        or policy_dict.get("reason")
        or "Input was not admitted by Input Policy Overlay."
    )

    preflight_event.update(
        {
            "mode": mode,
            "admitted": False,
            "action": policy_dict.get("decision", "INPUT_POLICY_NOT_ADMITTED"),
            "boundary_applied": boundary_applied,
            "should_call_llm": False,
            "llm_called": False,
            "final_response": message,
            "application_response": {
                "message": message,
                "should_call_llm": False,
                "boundary_applied": boundary_applied,
            },
        }
    )

    return preflight_event
