from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


"""
ACA Runtime v2 — Precondition Gate v0.2

Purpose:
This gate does not exercise full criterion.
It decides whether an input may enter semantic state.

Core invariant:
A non-admitted input must never alter semantic origin
or accepted trajectory.

TODO Runtime v2:
- Review transversal/rhetorical axis handling.
- Currently T always returns rhetorical because only one transversal artifact exists.
- Do not treat T as a competitive classification until more transversal artifacts exist.
- Later display it as rhetorical_cost or transversal_signal rather than T classification.
"""


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
    "verify through official channels",
    "official channel",
    "official channels",
    "trusted channel",
    "independent channel",
    "contact support",
    "report suspicious",
    "avoid entering",
    "do not enter",
]


PROTECTIVE_TRAINING_TERMS = [
    "teach users",
    "train users",
    "training",
    "recognize",
    "avoid",
    "warn",
    "protect",
    "security awareness",
    "safe cybersecurity",
    "report suspicious",
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


MANIPULATIVE_PRESSURE_PATTERNS = [
    "make them comply",
    "make the user comply",
    "make them act immediately",
    "cannot ignore it",
    "whatever framing is necessary",
    "get the information from them",
    "without explaining why",
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


def lower_text(text: str) -> str:
    return text.lower()


def contains_any(text: str, terms: List[str]) -> bool:
    lower = lower_text(text)
    return any(term in lower for term in terms)


def collect_hits(text: str, terms: List[str]) -> List[str]:
    lower = lower_text(text)
    return [
        term
        for term in terms
        if term in lower
    ]


def get_summary(measurements: Dict[str, Any]) -> Dict[str, Any]:
    return measurements.get("summary", {}) if measurements else {}


def atlas_signal(measurements: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts compact Atlas v2 F-C-P signals.

    This does not decide by itself.
    It provides supporting context for the gate.
    """

    summary = get_summary(measurements)

    return {
        "F": summary.get("F"),
        "C": summary.get("C"),
        "P": summary.get("P"),
        "T": summary.get("T"),
        "F_margin": summary.get("F_margin"),
        "C_margin": summary.get("C_margin"),
        "P_margin": summary.get("P_margin"),
        "T_margin": summary.get("T_margin"),
    }


def is_atlas_manipulation_exploit(
    signal: Dict[str, Any],
) -> bool:
    return (
        signal.get("C") == "manipulation"
        and signal.get("P") == "exploit"
    )


def is_atlas_protective(
    signal: Dict[str, Any],
) -> bool:
    return signal.get("P") == "protect"


def is_low_margin_signal(
    signal: Dict[str, Any],
    margin_threshold: float = 0.04,
) -> bool:
    margins = [
        signal.get("F_margin"),
        signal.get("C_margin"),
        signal.get("P_margin"),
    ]

    numeric = [
        margin
        for margin in margins
        if isinstance(margin, (int, float))
    ]

    if not numeric:
        return False

    return any(margin < margin_threshold for margin in numeric)


def detect_access_request(text: str) -> Dict[str, Any]:
    sensitive_hits = collect_hits(text, SENSITIVE_ACCESS_TERMS)
    verb_hits = collect_hits(text, ACCESS_REQUEST_VERBS)
    urgency_hits = collect_hits(text, URGENCY_TERMS)
    safe_hits = collect_hits(text, SAFE_VERIFICATION_TERMS)
    protective_hits = collect_hits(text, PROTECTIVE_TRAINING_TERMS)

    has_sensitive = bool(sensitive_hits)
    has_request_verb = bool(verb_hits)
    has_urgency = bool(urgency_hits)
    has_safe_context = bool(safe_hits)
    has_protective_training = bool(protective_hits)

    is_access_request = (
        has_sensitive
        and has_request_verb
        and not has_safe_context
        and not has_protective_training
    )

    return {
        "is_access_request": is_access_request,
        "has_sensitive": has_sensitive,
        "has_request_verb": has_request_verb,
        "has_urgency": has_urgency,
        "has_safe_context": has_safe_context,
        "has_protective_training": has_protective_training,
        "sensitive_hits": sensitive_hits,
        "verb_hits": verb_hits,
        "urgency_hits": urgency_hits,
        "safe_hits": safe_hits,
        "protective_hits": protective_hits,
    }


def detect_safe_access_context(text: str) -> Dict[str, Any]:
    sensitive_hits = collect_hits(text, SENSITIVE_ACCESS_TERMS)
    safe_hits = collect_hits(text, SAFE_VERIFICATION_TERMS)
    protective_hits = collect_hits(text, PROTECTIVE_TRAINING_TERMS)

    is_safe_access_context = (
        bool(sensitive_hits)
        and (
            bool(safe_hits)
            or bool(protective_hits)
        )
    )

    return {
        "is_safe_access_context": is_safe_access_context,
        "sensitive_hits": sensitive_hits,
        "safe_hits": safe_hits,
        "protective_hits": protective_hits,
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


def detect_manipulative_pressure(text: str) -> Dict[str, Any]:
    hits = collect_hits(text, MANIPULATIVE_PRESSURE_PATTERNS)

    return {
        "has_manipulative_pressure": bool(hits),
        "hits": hits,
    }


def decision(
    state: str,
    reason: str,
    allow_state_mutation: bool,
    allow_triaxial_projection: bool,
    allow_generation: bool,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> PreconditionDecision:
    return PreconditionDecision(
        state=state,
        reason=reason,
        allow_state_mutation=allow_state_mutation,
        allow_triaxial_projection=allow_triaxial_projection,
        allow_generation=allow_generation,
        tags=tags or [],
        metadata=metadata or {},
    )


def evaluate_precondition(
    text: str,
    has_origin: bool,
    measurements: Optional[Dict[str, Any]] = None,
) -> PreconditionDecision:
    """
    Deterministic precondition gate v0.2.

    It combines:
    - predefined safety rules
    - under-contextualization checks
    - absurd/out-of-field markers
    - compact Atlas F-C-P signals

    It does not exercise full criterion.
    It only decides whether the input may enter semantic state.
    """

    measurements = measurements or {}
    signal = atlas_signal(measurements)

    access = detect_access_request(text)
    safe_access = detect_safe_access_context(text)
    under_context = detect_under_contextualized(text)
    out_of_field = detect_absurd_or_out_of_field(text)
    pressure = detect_manipulative_pressure(text)

    metadata_base = {
        "atlas_signal": signal,
        "access": access,
        "safe_access": safe_access,
        "under_contextualized": under_context,
        "out_of_field": out_of_field,
        "pressure": pressure,
    }

    # 1. Absurd or out-of-field inputs stop before access policy.
    # This prevents isolated sensitive words inside nonsense from being
    # treated as valid credential requests.
    if out_of_field["is_absurd_or_out_of_field"]:
        return decision(
            state=FLAG_OUT_OF_FIELD,
            reason="Input appears semantically unstable or out of field.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "out_of_field",
                "semantic_instability",
            ],
            metadata=metadata_base,
        )

    # 2. Explicit credential/access extraction is a predefined risk.
    if access["is_access_request"]:
        return decision(
            state=REJECT_PREDEFINED_RISK,
            reason="Input requests sensitive access information.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "credential_request",
                "predefined_risk",
            ],
            metadata=metadata_base,
        )

    # 3. Safe training / verification around sensitive terms should not be
    # treated as exploitative access extraction.
    if safe_access["is_safe_access_context"]:
        return decision(
            state=BOUNDARY_RESPONSE,
            reason="Input discusses sensitive access information in a protective context.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=True,
            tags=[
                "safe_verification",
                "protective_context",
                "boundary_response",
            ],
            metadata=metadata_base,
        )

    # 4. Under-contextualized pressure should ask clarification before
    # becoming origin or continuation.
    if under_context["is_under_contextualized"]:
        tags = [
            "insufficient_context",
            "clarification_required",
        ]

        if is_atlas_manipulation_exploit(signal):
            tags.append("atlas_manipulation_exploit")

        return decision(
            state=ASK_CLARIFICATION,
            reason="Input is under-contextualized and should not become origin yet.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=tags,
            metadata=metadata_base,
        )

    # 5. Ambiguous manipulative pressure should not silently create origin.
    if pressure["has_manipulative_pressure"]:
        return decision(
            state=ASK_CLARIFICATION,
            reason="Input appears to request pressure or compliance without sufficient legitimate context.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "possible_manipulation",
                "insufficient_context",
                "clarification_required",
            ],
            metadata=metadata_base,
        )

    # 6. Atlas C=manipulation and P=exploit can support clarification,
    # but it must not automatically reject unless there is explicit access
    # extraction or predefined risk.
    if (
        is_atlas_manipulation_exploit(signal)
        and is_low_margin_signal(signal)
        and not has_origin
    ):
        return decision(
            state=ASK_CLARIFICATION,
            reason="Atlas detected manipulation/exploit orientation with low margin before a valid origin exists.",
            allow_state_mutation=False,
            allow_triaxial_projection=False,
            allow_generation=False,
            tags=[
                "atlas_manipulation_exploit",
                "low_margin",
                "clarification_required",
            ],
            metadata=metadata_base,
        )

    # 7. If no origin exists and no precondition blocks it, accept as origin.
    if not has_origin:
        return decision(
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
                "atlas_signal": signal,
            },
        )

    # 8. Otherwise accept as continuation.
    return decision(
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
            "atlas_signal": signal,
        },
    )