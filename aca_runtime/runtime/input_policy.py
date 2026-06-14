from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Mapping, Optional


DECISION_DEFER_ORIGIN_LOW_SIGNAL = "DEFER_ORIGIN_LOW_SIGNAL"
DECISION_ORIGIN_CANDIDATE = "ORIGIN_CANDIDATE"
DECISION_BOUNDARY_SECRET_REQUEST = "BOUNDARY_SECRET_REQUEST"
DECISION_BOUNDARY_MANIPULATION_REQUEST = "BOUNDARY_MANIPULATION_REQUEST"
DECISION_SAFE_CREDENTIAL_GUIDANCE = "SAFE_CREDENTIAL_GUIDANCE"
DECISION_ASK_CLARIFICATION_SENSITIVE = "ASK_CLARIFICATION_SENSITIVE"
DECISION_MONITOR_OR_ASK_CLARIFICATION = "MONITOR_OR_ASK_CLARIFICATION"


BOUNDARY_DECISIONS = {
    DECISION_BOUNDARY_SECRET_REQUEST,
    DECISION_BOUNDARY_MANIPULATION_REQUEST,
}


@dataclass(frozen=True)
class InputPolicyDecision:
    """Operational interpretation of an input before state mutation.

    The Atlas measures. The Runtime interprets. The Application decides.

    This object is intentionally policy-overlay oriented: it does not claim
    to verify truth or replace product policy. It only reports whether an
    input should be allowed to create origin, mutate trajectory, request
    clarification, receive safe guidance, or receive a boundary response.
    """

    decision: str
    reason: str
    state_mutation_allowed: bool
    origin_allowed: bool
    boundary_applied: bool
    response_envelope: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def get_nested(data: Mapping[str, Any], *path: str, default: Any = None) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, Mapping):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def classify_sensitive_intent(text: str) -> str:
    """Classify credential/secret-related intent using a small deterministic overlay.

    This is deliberately conservative. It separates direct extraction requests
    from defensive recovery/protection requests so that short sensitive inputs
    are not treated as ordinary low-signal inputs.
    """

    t = text.strip().lower()

    secret_terms = [
        "password",
        "contraseña",
        "contrasena",
        "token",
        "clave privada",
        "private key",
        "api key",
        "api keys",
        "secret key",
        "access token",
        "access tokens",
        "verification code",
        "verification codes",
        "credential",
        "credentials",
        "código de acceso",
        "codigo de acceso",
        "clave de acceso",
    ]

    extraction_markers = [
        "dame",
        "pásame",
        "pasame",
        "mándame",
        "mandame",
        "envíame",
        "enviame",
        "cuál es tu",
        "cual es tu",
        "cuál es el",
        "cual es el",
        "send me",
        "give me",
        "show me",
        "tell me your",
        "provide your",
        "share your",
        "need your",
        "enter your",
        "enter their",
        "submit your",
        "submit their",
    ]

    defensive_markers = [
        "cómo recupero",
        "como recupero",
        "recuperar mi",
        "restablecer mi",
        "resetear mi",
        "cómo protejo",
        "como protejo",
        "proteger mi",
        "me llegó",
        "me llego",
        "recibí",
        "recibi",
        "qué hago",
        "que hago",
        "cómo sé si",
        "como se si",
        "reportar",
        "bloquear",
        "how do i recover",
        "how can i recover",
        "recover my",
        "reset my",
        "reset password",
        "reset my password",
        "recover my password",
        "what should i do",
        "password was stolen",
        "stolen",
        "safely",
        "protect my",
        "secure my",
        "phishing check",
        "phishing report",
        "suspicious",
        "sospechoso",
        "falso",
    ]

    has_secret = any(term in t for term in secret_terms)
    is_extraction = any(marker in t for marker in extraction_markers)
    is_defensive = any(marker in t for marker in defensive_markers)

    if has_secret and is_extraction:
        return "SENSITIVE_DIRECT_EXTRACTION"

    if has_secret and is_defensive:
        return "SENSITIVE_DEFENSIVE_HELP"

    if has_secret:
        return "SENSITIVE_AMBIGUOUS"

    if is_defensive:
        return "DEFENSIVE_SECURITY_HELP"

    return "NOT_SENSITIVE"


def classify_manipulation_intent(text: str) -> bool:
    """Detect explicit manipulation, impersonation, coercion, or urgency pressure."""

    t = text.strip().lower()

    manipulation_markers = [
        "so the user does not have time to think",
        "use fear",
        "pressure the user",
        "pretending to be",
        "impersonate",
        "make the message urgent",
        "make the message more convincing",
        "more convincing so they click",
        "write a phishing message",
        "phishing message",
        "credential theft",
        "credential theft script",
        "bypass password",
        "bypass password verification",
        "pressures them to enter credentials",
        "make users enter their password",
        "account suspension",
        "convince someone to",
        "urgente para que",
        "sin que tenga tiempo de pensar",
        "usar miedo",
        "presionar",
        "hacerme pasar por",
        "fingiendo ser",
        "suspensión de cuenta",
        "suspension de cuenta",
    ]

    return any(marker in t for marker in manipulation_markers)


def build_safe_envelope(decision: str) -> str:
    if decision == DECISION_SAFE_CREDENTIAL_GUIDANCE:
        return (
            "Sensitive credential-related request detected. "
            "Respond only with safe account-recovery or account-protection guidance. "
            "Do not provide, request, infer, expose, or help obtain passwords, tokens, "
            "private keys, access codes, API keys, or secrets. "
            "Guide the user to official recovery channels, identity verification, "
            "password reset, MFA activation, phishing checks, and reporting suspicious messages."
        )

    if decision == DECISION_BOUNDARY_SECRET_REQUEST:
        return (
            "Direct request for credentials or secrets detected. "
            "Do not provide or help obtain passwords, tokens, private keys, access codes, "
            "API keys, or secrets. Respond with a safety boundary and, if useful, "
            "offer safe account-protection guidance."
        )

    if decision == DECISION_BOUNDARY_MANIPULATION_REQUEST:
        return (
            "Manipulation, impersonation, coercion, or urgency-pressure request detected. "
            "Do not help craft deceptive or coercive content. Offer safe alternatives such as "
            "security awareness, anti-phishing review, user-protection guidance, or transparent communication."
        )

    if decision == DECISION_ASK_CLARIFICATION_SENSITIVE:
        return (
            "Sensitive credential-related signal detected but intent is ambiguous. "
            "Ask whether the user is trying to recover/protect their own account or requesting access "
            "to credentials. Do not provide credential-extraction assistance."
        )

    return ""


def summarize_measurements(measurements: Mapping[str, Any]) -> Dict[str, Any]:
    summary = measurements.get("summary", {}) or {}

    return {
        "F": summary.get("F"),
        "C": summary.get("C"),
        "P": summary.get("P"),
        "T": summary.get("T"),
        "F_margin": summary.get("F_margin"),
        "C_margin": summary.get("C_margin"),
        "P_margin": summary.get("P_margin"),
        "foundation_cost": get_nested(measurements, "foundation", "top_cost"),
        "context_cost": get_nested(measurements, "context", "top_cost"),
        "principle_cost": get_nested(measurements, "principle", "top_cost"),
    }


def interpret_input_policy(
    text: str,
    measurements: Mapping[str, Any],
    *,
    low_margin_threshold: float = 0.03,
    high_cost_threshold: float = 0.90,
    semantic_margin_threshold: float = 0.07,
    risk_margin_threshold: float = 0.03,
) -> InputPolicyDecision:
    """Interpret Atlas measurements as an operational input policy decision.

    Current experimental rule:

    - high top-costs + low F/C/P margins -> defer origin;
    - manipulation + exploit signal -> inspect intent and route to boundary,
      safe guidance, or clarification;
    - semantically strong non-sensitive signal -> origin candidate;
    - remaining weak/ambiguous signal -> monitor or ask clarification.
    """

    m = summarize_measurements(measurements)

    f = m["F"]
    c = m["C"]
    p = m["P"]

    f_margin = m["F_margin"]
    c_margin = m["C_margin"]
    p_margin = m["P_margin"]

    margins = [x for x in [f_margin, c_margin, p_margin] if isinstance(x, (int, float))]
    costs = [
        x
        for x in [m["foundation_cost"], m["context_cost"], m["principle_cost"]]
        if isinstance(x, (int, float))
    ]

    low_margins = bool(margins) and all(x < low_margin_threshold for x in margins)
    high_costs = bool(costs) and all(x > high_cost_threshold for x in costs)

    sensitive_intent = classify_sensitive_intent(text)
    manipulation_intent = classify_manipulation_intent(text)

    # Risk requires coherent manipulation + exploit orientation.
    # A single weak manipulation margin should not turn neutral inputs like "ok"
    # into sensitive clarification.
    risk_signal = (
        c == "manipulation"
        and p == "exploit"
        and isinstance(c_margin, (int, float))
        and isinstance(p_margin, (int, float))
        and c_margin >= risk_margin_threshold
        and p_margin >= risk_margin_threshold
    )

    strong_semantic_margins = [
        x for x in margins
        if isinstance(x, (int, float)) and x >= semantic_margin_threshold
    ]
    semantic_margin_count = len(strong_semantic_margins)

    # Origin admission should not be created by one isolated margin.
    # It requires cross-axis support and no veto condition.
    semantic_signal = (
        semantic_margin_count >= 2
        and not risk_signal
        and sensitive_intent == "NOT_SENSITIVE"
        and not manipulation_intent
    )

    # Low signal is an interpretation of weak Atlas fit, not a word list.
    # High costs + no semantic/risk/sensitive/manipulation signal means:
    # application may receive the input, but it should not become origin.
    low_signal = (
        high_costs
        and not semantic_signal
        and not risk_signal
        and sensitive_intent == "NOT_SENSITIVE"
        and not manipulation_intent
    )

    if sensitive_intent == "SENSITIVE_DIRECT_EXTRACTION":
        decision = DECISION_BOUNDARY_SECRET_REQUEST
        reason = "The input directly requests credentials, secrets, tokens, keys, access codes, or verification codes."

    elif manipulation_intent and (risk_signal or sensitive_intent != "NOT_SENSITIVE"):
        decision = DECISION_BOUNDARY_MANIPULATION_REQUEST
        reason = "The input explicitly requests coercive, deceptive, credential-extractive, or bypass-oriented tactics."

    elif risk_signal:
        if sensitive_intent == "SENSITIVE_DEFENSIVE_HELP":
            decision = DECISION_SAFE_CREDENTIAL_GUIDANCE
            reason = "Atlas detected sensitive credential-related signal, but the declared intent is defensive or recovery-oriented."
        elif manipulation_intent:
            decision = DECISION_BOUNDARY_MANIPULATION_REQUEST
            reason = "Atlas detected manipulation/exploit orientation and the input explicitly requests coercive or deceptive tactics."
        elif sensitive_intent == "SENSITIVE_AMBIGUOUS":
            decision = DECISION_ASK_CLARIFICATION_SENSITIVE
            reason = "Atlas detected manipulation/exploit orientation with ambiguous credential-related intent."
        else:
            decision = DECISION_ASK_CLARIFICATION_SENSITIVE
            reason = "Atlas detected manipulation/exploit orientation without enough safe intent clarity."

    elif sensitive_intent == "SENSITIVE_DEFENSIVE_HELP":
        decision = DECISION_SAFE_CREDENTIAL_GUIDANCE
        reason = "The input is credential-related but framed as defensive help or account recovery."

    elif sensitive_intent == "SENSITIVE_AMBIGUOUS":
        decision = DECISION_ASK_CLARIFICATION_SENSITIVE
        reason = "Credential-related signal detected with ambiguous intent."

    elif low_signal:
        decision = DECISION_DEFER_ORIGIN_LOW_SIGNAL
        reason = "Top costs are high and no coherent semantic, risk, or sensitive signal justifies origin admission."

    elif sensitive_intent == "DEFENSIVE_SECURITY_HELP":
        decision = DECISION_ORIGIN_CANDIDATE
        reason = "The input asks for defensive security guidance without requesting credentials or secrets."

    elif semantic_signal:
        decision = DECISION_ORIGIN_CANDIDATE
        reason = "Cross-axis F/C/P support is strong enough to treat the input as a semantic origin candidate."

    elif manipulation_intent:
        decision = DECISION_BOUNDARY_MANIPULATION_REQUEST
        reason = "The input requests manipulative, coercive, exploitative, or deceptive tactics."

    else:
        decision = DECISION_MONITOR_OR_ASK_CLARIFICATION
        reason = "The signal is not strong enough for origin and not clearly low-signal or sensitive."

    boundary_applied = decision in BOUNDARY_DECISIONS
    origin_allowed = decision == DECISION_ORIGIN_CANDIDATE
    state_mutation_allowed = origin_allowed
    response_envelope = build_safe_envelope(decision)

    metadata = {
        **m,
        "low_margins": low_margins,
        "high_costs": high_costs,
        "low_signal": low_signal,
        "risk_signal": risk_signal,
        "semantic_signal": semantic_signal,
        "semantic_margin_count": semantic_margin_count,
        "sensitive_intent": sensitive_intent,
        "manipulation_intent": manipulation_intent,
        "low_margin_threshold": low_margin_threshold,
        "high_cost_threshold": high_cost_threshold,
        "semantic_margin_threshold": semantic_margin_threshold,
        "risk_margin_threshold": risk_margin_threshold,
    }

    return InputPolicyDecision(
        decision=decision,
        reason=reason,
        state_mutation_allowed=state_mutation_allowed,
        origin_allowed=origin_allowed,
        boundary_applied=boundary_applied,
        response_envelope=response_envelope,
        metadata=metadata,
    )
