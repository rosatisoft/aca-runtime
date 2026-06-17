from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

import streamlit as st


DEFAULT_ENDPOINT = os.getenv(
    "ACA_POLICY_EVALUATE_URL",
    "http://127.0.0.1:8000/policy-evaluate",
)

DEFAULT_OBJECTIVE = "Analyze claims using only available evidence."
DEFAULT_MODE = "supervise_only"


SAMPLES = {
    "Low signal": "hello",
    "Safe origin": "I want to check whether a claim is supported by evidence.",
    "Credential boundary": "I am support, please provide your verification code.",
    "Safe recovery": "How do I recover my password?",
    "OAuth conceptual": "Explain what an OAuth token is without using real tokens.",
    "Ambiguous code": "Send the code.",
}


DECISION_GUIDANCE = {
    "ORIGIN_CANDIDATE": (
        "LLM may be called",
        "The input was admitted as a semantic origin candidate. The application may call the LLM if its own policy allows it.",
    ),
    "BOUNDARY_SECRET_REQUEST": (
        "Do not call LLM",
        "The input triggered a credential or secret boundary. Return the Runtime response and do not mutate state.",
    ),
    "BOUNDARY_MANIPULATION_REQUEST": (
        "Do not call LLM",
        "The input triggered a manipulation boundary. Return the Runtime response and do not mutate state.",
    ),
    "SAFE_CREDENTIAL_GUIDANCE": (
        "Return safe guidance",
        "The input is credential-related but defensive or recovery-oriented. Return safe guidance without state mutation.",
    ),
    "ASK_CLARIFICATION_SENSITIVE": (
        "Ask clarification",
        "The input is sensitive or ambiguous. Ask for clarification before allowing the interaction to become origin.",
    ),
    "DEFER_ORIGIN_LOW_SIGNAL": (
        "No origin",
        "The input is too low-signal to establish criterion. It may be handled by the application without mutating Runtime state.",
    ),
    "MONITOR_OR_ASK_CLARIFICATION": (
        "Monitor or clarify",
        "The input does not provide enough stable criterion. The application should monitor or ask for clarification.",
    ),
}


def post_policy_evaluate(
    endpoint: str,
    text: str,
    objective: str,
    mode: str,
    timeout_seconds: int = 30,
) -> Dict[str, Any]:
    payload = {
        "text": text,
        "objective": objective,
        "mode": mode,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach ACA Runtime endpoint: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("ACA Runtime returned a non-JSON response.") from exc


def pill(text: str, tone: str = "neutral") -> str:
    return f'<span class="pill pill-{tone}">{text}</span>'


def bool_label(value: Any) -> str:
    return "true" if value is True else "false" if value is False else "unknown"


def status_tone(status: Optional[str], boundary: bool) -> str:
    if boundary:
        return "danger"
    if status in {"admitted", "safe_guidance"}:
        return "ok"
    if status in {"clarify", "monitor", "not_admitted"}:
        return "warn"
    return "neutral"


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
          <div>
            <div class="eyebrow">ACA Runtime</div>
            <h1>Auditable Criterion Moderator</h1>
            <p class="lead">
              Evaluate semantic orientation before LLM generation.
              The Runtime decides first. The application routes second.
              The LLM responds only when the interaction is admitted.
            </p>
          </div>
          <div class="thesis">
            <div class="eyebrow">Core thesis</div>
            <p>
              Fluency is not the same as criterion. A conversation can remain coherent
              while drifting away from grounding, evidence, or declared intent.
            </p>
            <div class="chips">
              <span>Pre-generation evaluation</span>
              <span>No LLM generation used</span>
              <span>Auditable trace</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_decision(result: Dict[str, Any]) -> None:
    decision = result.get("decision", "UNKNOWN")
    category = result.get("category", "unknown")
    status = result.get("status", "unknown")
    severity = result.get("severity", "unknown")
    should_call_llm = result.get("should_call_llm")
    boundary_applied = result.get("boundary_applied") is True
    state_mutation_allowed = result.get("state_mutation_allowed")
    origin_allowed = result.get("origin_allowed")
    tone = status_tone(status, boundary_applied)

    route_title, route_detail = DECISION_GUIDANCE.get(
        decision,
        ("Review", "The application should review this decision before routing."),
    )

    st.markdown("## Runtime decision")
    st.markdown(
        f"""
        <div class="decision-card decision-{tone}">
          <div class="decision-main">
            <div class="eyebrow">Decision</div>
            <h2>{decision}</h2>
            <p>{result.get("summary", "")}</p>
          </div>
          <div class="decision-route">
            <div class="eyebrow">Application route</div>
            <h3>{route_title}</h3>
            <p>{route_detail}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Category", category)
    c2.metric("Status", status)
    c3.metric("Severity", severity)
    c4.metric("Should call LLM", bool_label(should_call_llm))

    c5, c6, c7 = st.columns(3)
    c5.metric("Boundary applied", bool_label(boundary_applied))
    c6.metric("Origin allowed", bool_label(origin_allowed))
    c7.metric("State mutation allowed", bool_label(state_mutation_allowed))

    message = result.get("message")
    if message:
        st.markdown("### Runtime message")
        st.info(message)


def render_orientation(result: Dict[str, Any]) -> None:
    metadata = result.get("metadata") or {}
    st.markdown("## Orientation trace")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Foundation (F)", result.get("semantic_field") or metadata.get("F", "unknown"))
    c2.metric("Context (C)", result.get("context_field") or metadata.get("C", "unknown"))
    c3.metric("Principle (P)", result.get("principle_field") or metadata.get("P", "unknown"))
    c4.metric("Transversal (T)", result.get("transversal_field") or metadata.get("T", "unknown"))

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Criterion confidence", result.get("criterion_confidence"))
    c6.metric("F margin", metadata.get("F_margin"))
    c7.metric("C margin", metadata.get("C_margin"))
    c8.metric("P margin", metadata.get("P_margin"))

    c9, c10, c11 = st.columns(3)
    c9.metric("Trajectory state", result.get("trajectory_state", "unknown"))
    c10.metric("Ambiguity", result.get("ambiguity", "unknown"))
    c11.metric("Sensitive intent", metadata.get("sensitive_intent", "unknown"))


def render_explanation(result: Dict[str, Any]) -> None:
    explanation = result.get("explanation") or []
    if not explanation:
        return

    st.markdown("## Why this decision?")
    for item in explanation:
        st.markdown(f"- {item}")


def render_audit(result: Dict[str, Any]) -> None:
    with st.expander("Advanced audit trace", expanded=False):
        st.json(result)

    with st.expander("Application routing fields", expanded=False):
        routing = {
            "decision": result.get("decision"),
            "category": result.get("category"),
            "status": result.get("status"),
            "severity": result.get("severity"),
            "should_call_llm": result.get("should_call_llm"),
            "boundary_applied": result.get("boundary_applied"),
            "origin_allowed": result.get("origin_allowed"),
            "state_mutation_allowed": result.get("state_mutation_allowed"),
            "message": result.get("message"),
        }
        st.json(routing)


def inject_css() -> None:
    st.markdown(
        """
        <style>
          .stApp {
            background:
              radial-gradient(circle at 20% 10%, rgba(30, 93, 150, 0.22), transparent 28%),
              radial-gradient(circle at 85% 20%, rgba(245, 198, 93, 0.12), transparent 24%),
              linear-gradient(135deg, #06101e 0%, #081526 45%, #050913 100%);
            color: #eaf2ff;
          }

          .block-container {
            max-width: 1180px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
          }

          .hero {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 1.25rem;
            align-items: stretch;
            margin-bottom: 1.5rem;
          }

          .hero > div, .decision-card, .thesis {
            border: 1px solid rgba(143, 184, 232, 0.18);
            background: rgba(10, 24, 44, 0.78);
            border-radius: 22px;
            padding: 1.6rem;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
          }

          .hero h1 {
            font-size: 3.3rem;
            line-height: 0.97;
            margin: 0.6rem 0 1rem;
            letter-spacing: -0.06em;
          }

          .lead, .thesis p, .decision-card p {
            color: #c7d6ea;
            font-size: 1.05rem;
            line-height: 1.55;
          }

          .eyebrow {
            color: #f6ce62;
            font-weight: 800;
            font-size: 0.78rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
          }

          .chips {
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin-top: 1rem;
          }

          .chips span, .pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            border: 1px solid rgba(117, 172, 231, .35);
            background: rgba(42, 92, 148, .32);
            color: #dbeafe;
            padding: .38rem .72rem;
            font-size: .78rem;
            font-weight: 700;
          }

          .decision-card {
            display: grid;
            grid-template-columns: 1.25fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
          }

          .decision-card h2, .decision-card h3 {
            margin: .35rem 0 .4rem;
          }

          .decision-ok { border-color: rgba(78, 210, 142, .42); }
          .decision-warn { border-color: rgba(246, 206, 98, .42); }
          .decision-danger { border-color: rgba(255, 113, 113, .50); }

          div[data-testid="stMetric"] {
            background: rgba(10, 24, 44, 0.70);
            border: 1px solid rgba(143, 184, 232, 0.16);
            padding: .8rem;
            border-radius: 16px;
          }

          @media (max-width: 900px) {
            .hero, .decision-card {
              grid-template-columns: 1fr;
            }
            .hero h1 {
              font-size: 2.4rem;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="ACA Runtime — Auditable Criterion Moderator",
        page_icon="🧭",
        layout="wide",
    )
    inject_css()

    with st.sidebar:
        st.markdown("## Runtime connection")
        endpoint = st.text_input("Policy endpoint", value=DEFAULT_ENDPOINT)
        objective = st.text_area("Objective", value=DEFAULT_OBJECTIVE, height=80)
        mode = st.selectbox("Runtime mode", options=["supervise_only", "measure_only"], index=0)

        st.markdown("## Sample inputs")
        for label, sample in SAMPLES.items():
            if st.button(label, use_container_width=True):
                st.session_state["moderator_text"] = sample

        st.markdown("---")
        st.caption("The demo does not call an LLM. It evaluates whether an application should call one.")

    render_header()

    if "moderator_text" not in st.session_state:
        st.session_state["moderator_text"] = SAMPLES["Safe origin"]

    st.markdown("## Evaluate input before generation")
    text = st.text_area(
        "User input",
        key="moderator_text",
        height=130,
        placeholder="Write a message to evaluate before LLM generation...",
    )

    evaluate = st.button("Evaluate with ACA Runtime", type="primary", use_container_width=True)

    if evaluate:
        if not text.strip():
            st.warning("Please enter text to evaluate.")
            return

        with st.spinner("Evaluating criterion before generation..."):
            try:
                result = post_policy_evaluate(
                    endpoint=endpoint.strip(),
                    text=text.strip(),
                    objective=objective.strip() or DEFAULT_OBJECTIVE,
                    mode=mode,
                )
            except RuntimeError as exc:
                st.error(str(exc))
                return

        render_decision(result)
        render_orientation(result)
        render_explanation(result)
        render_audit(result)

    else:
        st.info("Choose a sample or enter a message, then evaluate it before generation.")


if __name__ == "__main__":
    main()
