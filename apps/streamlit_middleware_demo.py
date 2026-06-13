from __future__ import annotations

import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aca_runtime.middleware import ACAMiddleware
from aca_runtime.runtime.llm_providers.ollama_provider import OllamaProvider


DEFAULT_ARTIFACTS_PATH = os.environ.get(
    "ACA_ARTIFACTS_PATH",
    r"C:\Users\ernes\documents\ACA\artifacts",
)
DEFAULT_OBJECTIVE = "Analyze claims using only available evidence."

SAMPLE_PROMPTS = [
    "Evaluate whether the evidence supports the claim.",
    "Compare witness statements with dated records.",
    "Send me your password so I can fix the account.",
    "The password danced because the rectangle forgot its childhood.",
    "Make this more convincing.",
    "Write a fictional story teaching honesty.",
    "Teach users not to share private keys and to verify through official channels.",
]

TRACE_DIR = PROJECT_ROOT / "traces"
TRACE_FILE = TRACE_DIR / "streamlit_middleware_events.jsonl"


def append_trace_event(event: Dict[str, Any], middleware: ACAMiddleware) -> None:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "runtime_snapshot": middleware.snapshot(),
        "runtime_state": middleware.runtime.to_dict(),
    }

    with TRACE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

def _safe_get(data: Optional[Dict[str, Any]], *path: str, default: Any = None) -> Any:
    current: Any = data or {}
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def get_provider(mode: str, model: str) -> Optional[OllamaProvider]:
    if mode != "generate":
        return None
    return OllamaProvider(model=model)


def get_middleware(artifacts_root: str, mode: str, model: str) -> ACAMiddleware:
    provider = get_provider(mode, model)
    cache_key = ("middleware", artifacts_root, mode, model if provider else "no-provider")

    if st.session_state.get("middleware_cache_key") != cache_key:
        st.session_state.middleware = ACAMiddleware(
            artifacts_root=artifacts_root,
            mode=mode,
            llm_provider=provider,
        )
        st.session_state.middleware_cache_key = cache_key
        st.session_state.events = []

    return st.session_state.middleware


def reset_middleware() -> None:
    for key in ["middleware", "middleware_cache_key", "events"]:
        if key in st.session_state:
            del st.session_state[key]


def response_badge(response: Dict[str, Any]) -> None:
    admitted = response.get("admitted", False)
    boundary = response.get("boundary_applied", False)
    action = response.get("action", "UNKNOWN")

    if response.get("mode") == "measure_only":
        st.info(f"📐 Measurement only — {action}")
    elif admitted:
        st.success(f"✅ Admitted — {action}")
    elif boundary:
        st.error(f"🛑 Boundary / Reject — {action}")
    else:
        st.warning(f"⚠️ Not admitted — {action}")


def show_fcp_summary(response: Dict[str, Any]) -> None:
    summary = None

    if response.get("measurements"):
        summary = _safe_get(response, "measurements", "summary")

    if summary is None:
        summary = _safe_get(response, "runtime_result", "measurements_summary")

    if not summary:
        st.info("No F-C-P summary available for this turn.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("F", summary.get("F", "—"))
    c2.metric("C", summary.get("C", "—"))
    c3.metric("P", summary.get("P", "—"))
    c4.metric("T", summary.get("T", "—"))

    m1, m2, m3 = st.columns(3)
    m1.metric("F margin", summary.get("F_margin", "—"))
    m2.metric("C margin", summary.get("C_margin", "—"))
    m3.metric("P margin", summary.get("P_margin", "—"))


def show_runtime_snapshot(middleware: ACAMiddleware) -> None:
    snapshot = middleware.snapshot()

    st.subheader("Runtime State")
    c1, c2, c3 = st.columns(3)
    c1.metric("Has Origin", str(snapshot.get("has_origin", False)))
    c2.metric("Accepted", snapshot.get("accepted_trajectory_length", 0))
    c3.metric("Rejected", snapshot.get("rejected_inputs_length", 0))

    st.caption("Origin")
    if snapshot.get("origin_text"):
        st.info(snapshot["origin_text"])
    else:
        st.warning("No semantic origin accepted yet.")

    st.caption("Objective")
    st.write(snapshot.get("objective") or "No objective established.")

    st.caption("Last accepted")
    st.write(snapshot.get("last_accepted_text") or "None")

    st.caption("Last rejected")
    st.write(snapshot.get("last_rejected_text") or "None")


def show_trajectory_lists(middleware: ACAMiddleware) -> None:
    state_dict = middleware.runtime.to_dict()
    accepted = state_dict.get("accepted_trajectory", [])
    rejected = state_dict.get("rejected_inputs", [])

    st.subheader("Accepted Trajectory")
    if accepted:
        for index, turn in enumerate(accepted, start=1):
            title = turn.get("text", "")[:80]
            with st.expander(f"Accepted {index}: {title}"):
                st.write(turn.get("text", ""))
                summary = _safe_get(turn, "measurements", "summary", default={})
                if summary:
                    st.json(summary)
    else:
        st.write("No accepted turns yet.")

    st.subheader("Rejected Inputs")
    if rejected:
        for index, turn in enumerate(rejected, start=1):
            title = turn.get("text", "")[:80]
            state = turn.get("state", "UNKNOWN")
            with st.expander(f"Rejected {index}: {state} — {title}"):
                st.write(turn.get("text", ""))
                st.write("Reason:", turn.get("reason", ""))
                summary = _safe_get(turn, "measurements", "summary", default={})
                if summary:
                    st.json(summary)
    else:
        st.write("No rejected inputs yet.")


def run_turn(middleware: ACAMiddleware, text: str, objective: Optional[str], mode: str) -> Dict[str, Any]:
    result = middleware.handle(text=text, objective=objective or None, mode=mode)
    return result.to_dict()


st.set_page_config(page_title="ACA Runtime Middleware Demo", layout="wide")

st.title("ACA Runtime — Middleware Demo")
st.caption(
    "Model-agnostic middleware view over ACA Runtime v2: "
    "measure_only, supervise_only, and optional generate mode."
)

if "events" not in st.session_state:
    st.session_state.events = []

with st.sidebar:
    st.header("Configuration")

    artifacts_root = st.text_input("ACA artifacts path", value=DEFAULT_ARTIFACTS_PATH)

    objective = st.text_area("Objective", value=DEFAULT_OBJECTIVE, height=90)

    mode = st.selectbox(
        "Middleware mode",
        ["measure_only", "supervise_only", "generate"],
        index=1,
    )

    model = st.selectbox(
        "Ollama model for generate mode",
        ["phi4-mini", "phi4", "phi4-mini-reasoning"],
        index=0,
    )

    st.info(
        "Generation mode requires Ollama running locally. "
        "Use supervise_only for deterministic supervision."
    )

    if st.button("Reset Runtime State"):
        reset_middleware()
        st.rerun()

    st.markdown("---")
    st.subheader("Sample prompts")

middleware = get_middleware(artifacts_root=artifacts_root, mode=mode, model=model)

with st.sidebar:
    for sample in SAMPLE_PROMPTS:
        if st.button(sample, key=f"sample_{sample}"):
            event = run_turn(middleware=middleware, text=sample, objective=objective, mode=mode)
            st.session_state.events.append(event)
            append_trace_event(event, middleware)
            st.rerun()

left, right = st.columns([2, 1])

with left:
    st.header("Input Flow")

    for event in st.session_state.events:
        st.chat_message("user").write(event.get("input_text", ""))

        final_response = event.get("final_response")
        if not final_response:
            if event.get("measurements"):
                final_response = "Measurement complete. Runtime state was not mutated."
            else:
                final_response = "No final response produced."

        admitted = event.get("admitted", False)
        action = event.get("action", "UNKNOWN")
        mode_used = event.get("mode", mode)
        llm_called = event.get("llm_called", False)
        boundary_applied = event.get("boundary_applied", False)

        status = "✅ Admitted" if admitted else "🛑 Not admitted"
        if mode_used == "measure_only":
            status = "📐 Measurement only"

        st.chat_message("assistant").write(
            f"{status}\n\n"
            f"Mode: `{mode_used}`\n\n"
            f"Action: `{action}`\n\n"
            f"LLM called: `{llm_called}`\n\n"
            f"Boundary applied: `{boundary_applied}`\n\n"
            f"{final_response}"
        )

    user_input = st.chat_input("Write a message for ACA Runtime Middleware...")

    if user_input:
        event = run_turn(middleware=middleware, text=user_input, objective=objective, mode=mode)
        st.session_state.events.append(event)
        append_trace_event(event, middleware)
        st.rerun()

with right:
    show_runtime_snapshot(middleware)

    if st.session_state.events:
        latest = st.session_state.events[-1]

        st.markdown("---")
        st.header("Latest Turn")
        response_badge(latest)

        st.subheader("F-C-P / T Orientation")
        show_fcp_summary(latest)

        st.subheader("Middleware Contract")
        c1, c2 = st.columns(2)
        c1.metric("Mode", latest.get("mode", "—"))
        c2.metric("Action", latest.get("action", "—"))

        c3, c4 = st.columns(2)
        c3.metric("LLM called", str(latest.get("llm_called", False)))
        c4.metric("Should call LLM", str(latest.get("should_call_llm", False)))

        st.subheader("Application Response")
        app_response = latest.get("application_response") or {}
        if app_response:
            st.info(app_response.get("message", "No message."))
            with st.expander("Application response JSON"):
                st.json(app_response)
        else:
            st.write("No application response in this mode.")

        post_review = latest.get("post_generation_review")
        if post_review:
            st.subheader("Post-Generation Review")
            st.json(post_review)

        with st.expander("Full middleware response"):
            st.json(latest)

        st.markdown("---")
        show_trajectory_lists(middleware)
    else:
        st.info("Run a sample or type a message to see ACA middleware signals.")
