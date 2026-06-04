from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


ACCEPT_AS_ORIGIN = "ACCEPT_AS_ORIGIN"
ACCEPT_AS_CONTINUATION = "ACCEPT_AS_CONTINUATION"
ASK_CLARIFICATION = "ASK_CLARIFICATION"
DECLARE_INTENT = "DECLARE_INTENT"
BOUNDARY_RESPONSE = "BOUNDARY_RESPONSE"
REJECT_PREDEFINED_RISK = "REJECT_PREDEFINED_RISK"
FLAG_OUT_OF_FIELD = "FLAG_OUT_OF_FIELD"
CONTINUE_MONITORING = "CONTINUE_MONITORING"


SENSITIVE_ACCESS_TERMS = [
    "password",
    "pin",
    "private key",
    "secret token",
    "access token",
    "access code",
    "verification code",
    "credential",
    "credentials",
    "username",
    "login information",
]


ACCESS_REQUEST_VERBS = [
    "send",
    "provide",
    "enter",
    "share",
    "submit",
    "reveal",
    "give me",
    "verify",
    "type",
    "input",
]


URGENCY_TERMS = [
    "immediately",
    "now",
    "urgent",
    "suspended",
    "suspension",
    "disabled",
    "permanently disabled",
    "avoid losing access",
    "failure to comply",
    "within the next hour",
]


SAFE_VERIFICATION_TERMS = [
    "do not share",
    "never ask",
    "verify through official",
    "official channel",
    "trusted channel",
    "independent channel",
    "contact support",
]


UNDER_CONTEXTUALIZED_PATTERNS = [
    "make this more convincing",
    "make it stronger",
    "help me with this",
    "fix this",
    "make them comply",
    "get them to agree",
    "make the message stronger",
]


ABSURD_MARKERS = [
    "rectangle forgot",
    "password danced",
    "yesterday is a database",
    "moon authenticated",
    "soup with invisible arithmetic",
    "conclusion became triangular",
]


@dataclass
class PreconditionDecision:
    state: str
    reason: str
    allow_state_mutation: bool
    allow_triaxial_projection: bool
    allow_generation: bool
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def contains_any(text: str, terms: List[str]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def collect_hits(text: str, terms: List[str]) -> List[str]:
    lower = text.lower()
    return [
        term
        for term in terms
        if term in lower
    ]


def detect_access_request(text: str) -> Dict[str, Any]:
    lower = text.lower()

    sensitive_hits = collect_hits(lower, SENSITIVE_ACCESS_TERMS)
    verb_hits = collect_hits(lower, ACCESS_REQUEST_VERBS)
    urgency_hits = collect_hits(lower, URGENCY_TERMS)
    safe_hits = collect_hits(lower, SAFE_VERIFICATION_TERMS)

    has_sensitive = bool(sensitive_hits)
    has_request_verb = bool(verb_hits)
    has_urgency = bool(urgency_hits)
    has_safe_context = bool(safe_hits)

    is_access_request = (
        has_sensitive
        and has_request_verb
        and not has_safe_context
    )

    return {
        "is_access_request": is_access_request,
        "has_sensitive": has_sensitive,
        "has_request_verb": has_request_verb,
        "has_urgency": has_urgency,
        "has_safe_context": has_safe_context,
        "sensitive_hits": sensitive_hits,
        "verb_hits": verb_hits,
        "urgency_hits": urgency_hits,
        "safe_hits": safe_hits,
    }


def detect_under_contextualized(text: str) -> Dict[str, Any]:
    hits = collect_hits(text, UNDER_CONTEXTUALIZED_PATTERNS)

    return {
        "is_under_contextualized": bool(hits),
        "hits": hits,
    }


def detect_absurd_or_out_of_field(text: str) -> Dict[str, Any]:
    hits = collect_hits(text, ABSURD_MARKERS)

    return {
        "is_absurd_or_out_of_field": bool(hits),
        "hits": hits,
    }


def evaluate_precondition(
    text: str,
    has_origin: bool,
    measurements: Optional[Dict[str, Any]] = None,
) -> PreconditionDecision:
    """
    Deterministic precondition gate.

    This first version only decides whether the input may create or update
    semantic state. Later versions will incorporate Atlas measurements:
    origin_cost, field coverage, structural orientation, intent, and F-C-P.
    """

    measurements = measurements or {}

    access = detect_access_request(text)
    under_context = detect_under_contextualized(text)
    out_of_field = detect_absurd_or_out_of_field(text)

    if access["is_access_request"]:
        return PreconditionDecision(
            state=REJECT_PREDEFINED_RISK,
            reason="Input requests sensitive access information.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "credential_request",
                "predefined_risk",
            ],
            metadata={
                "access": access,
            },
        )

    if access["has_sensitive"] and access["has_safe_context"]:
        return PreconditionDecision(
            state=BOUNDARY_RESPONSE,
            reason="Input discusses sensitive access information in a protective context.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=True,
            tags=[
                "safe_verification",
                "boundary_response",
            ],
            metadata={
                "access": access,
            },
        )

    if out_of_field["is_absurd_or_out_of_field"]:
        return PreconditionDecision(
            state=FLAG_OUT_OF_FIELD,
            reason="Input appears semantically unstable or out of field.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "out_of_field",
                "semantic_instability",
            ],
            metadata={
                "out_of_field": out_of_field,
            },
        )

    if under_context["is_under_contextualized"]:
        return PreconditionDecision(
            state=ASK_CLARIFICATION,
            reason="Input is under-contextualized and should not become origin yet.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "insufficient_context",
                "clarification_required",
            ],
            metadata={
                "under_contextualized": under_context,
            },
        )

    if not has_origin:
        return PreconditionDecision(
            state=ACCEPT_AS_ORIGIN,
            reason="Input accepted as semantic origin.",
            allow_state_mutation=True,
            allow_triaxial_projection=True,
            allow_generation=True,
            tags=[
                "origin_candidate",
            ],
            metadata={
                "measurements": measurements,
            },
        )

    return PreconditionDecision(
        state=ACCEPT_AS_CONTINUATION,
        reason="Input accepted as trajectory continuation.",
        allow_state_mutation=True,
        allow_triaxial_projection=True,
        allow_generation=True,
        tags=[
            "continuation_candidate",
        ],
        metadata={
            "measurements": measurements,
        },
    )