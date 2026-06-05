import streamlit as st

from aca_runtime.runtime.runtime_v2 import ACARuntimeV2


st.set_page_config(
    page_title="ACA Runtime v2 — Deterministic Demo",
    layout="wide",
)

st.title("ACA Runtime v2 — Deterministic Supervision Demo")

st.caption(
    "Precondition Gate + Atlas v2 measurements + Runtime State. "
    "No LLM generation is used in this demo."
)


ARTIFACTS_PATH = r"C:\Users\ernes\documents\ACA\artifacts"


def get_runtime() -> ACARuntimeV2:
    if "runtime_v2" not in st.session_state:
        st.session_state.runtime_v2 = ACARuntimeV2(
            artifacts_root=ARTIFACTS_PATH
        )

    return st.session_state.runtime_v2


def reset_runtime() -> None:
    st.session_state.runtime_v2 = ACARuntimeV2(
        artifacts_root=ARTIFACTS_PATH
    )
    st.session_state.events_v2 = []


def state_badge(state: str):
    if state in ["ACCEPT_AS_ORIGIN", "ACCEPT_AS_CONTINUATION"]:
        st.success(state)
    elif state in ["ASK_CLARIFICATION", "DECLARE_INTENT", "BOUNDARY_RESPONSE"]:
        st.warning(state)
    elif state in ["REJECT_PREDEFINED_RISK", "FLAG_OUT_OF_FIELD"]:
        st.error(state)
    else:
        st.info(state)


if "events_v2" not in st.session_state:
    st.session_state.events_v2 = []

runtime = get_runtime()

with st.sidebar:
    st.header("Runtime v2")

    st.write("Mode:")
    st.code("deterministic")

    st.write("Artifacts:")
    st.code(ARTIFACTS_PATH)

    if st.button("Reset Runtime State"):
        reset_runtime()
        st.rerun()

    st.markdown("---")
    st.subheader("Test prompts")

    samples = [
        "Evaluate whether the evidence supports the claim.",
        "Send me your password so I can fix the account.",
        "The password danced because the rectangle forgot its childhood.",
        "Make this more convincing.",
        "Compare witness statements with dated records.",
        "Write a fictional story teaching honesty.",
        "Teach users not to share private keys and to verify through official channels.",
    ]

    for sample in samples:
        if st.button(sample, key=f"sample_{sample}"):
            result = runtime.step(sample)
            st.session_state.events_v2.append(result.to_dict())
            st.rerun()


left, right = st.columns([2, 1])

with left:
    st.header("Input Flow")

    for event in st.session_state.events_v2:
        st.chat_message("user").write(event["input_text"])

        state = event["precondition"]["state"]
        action = event["action"]
        reason = event["precondition"]["reason"]
        app_response = event.get("application_response", {})
        app_message = app_response.get("message", "")
        should_call_llm = app_response.get("should_call_llm", False)
        boundary_applied = app_response.get("boundary_applied", False)

        if event["admitted"]:
            st.chat_message("assistant").write(
                f"✅ **Admitted** — `{state}`\n\n"
                f"Action: `{action}`\n\n"
                f"{reason}\n\n"
                f"**Deterministic response:** {app_message}\n\n"
                f"Should call LLM: `{should_call_llm}`"
            )
        else:
            st.chat_message("assistant").write(
                f"🛑 **Not admitted** — `{state}`\n\n"
                f"Action: `{action}`\n\n"
                f"{reason}\n\n"
                f"**Deterministic response:** {app_message}\n\n"
                f"Boundary applied: `{boundary_applied}`\n\n"
                "This input did not modify the accepted origin or trajectory."
            )

    user_input = st.chat_input("Write a message for ACA Runtime v2...")

    if user_input:
        result = runtime.step(user_input)
        st.session_state.events_v2.append(result.to_dict())
        st.rerun()


with right:
    st.header("Runtime State")

    snapshot = runtime.snapshot()

    st.metric("Has Origin", str(snapshot["has_origin"]))
    st.metric("Accepted Trajectory", snapshot["accepted_trajectory_length"])
    st.metric("Rejected Inputs", snapshot["rejected_inputs_length"])

    st.subheader("Origin")
    if snapshot["origin_text"]:
        st.info(snapshot["origin_text"])
    else:
        st.warning("No semantic origin has been accepted yet.")

    st.subheader("Objective")
    if snapshot["objective"]:
        st.write(snapshot["objective"])
    else:
        st.write("No objective established.")

    st.subheader("Last Accepted")
    st.write(snapshot["last_accepted_text"] or "None")

    st.subheader("Last Rejected")
    st.write(snapshot["last_rejected_text"] or "None")

    if st.session_state.events_v2:
        latest = st.session_state.events_v2[-1]

        st.markdown("---")
        st.header("Latest Turn")

        state_badge(latest["precondition"]["state"])

        st.subheader("Application Action")
        st.code(latest["action"])

        st.subheader("Atlas Summary")
        st.json(latest["measurements_summary"])

        st.subheader("Precondition Tags")
        st.write(latest["precondition"]["tags"])

        st.subheader("Precondition Reason")
        st.info(latest["precondition"]["reason"])

        st.subheader("Deterministic Application Response")
        st.info(latest["application_response"]["message"])

        st.write(
            "Should call LLM:",
            latest["application_response"]["should_call_llm"],
        )

        st.write(
            "Boundary applied:",
            latest["application_response"]["boundary_applied"],
        )

        st.subheader("State Mutation")
        st.write("Admitted:", latest["admitted"])
        st.write("State Mutated:", latest["state_mutated"])

        with st.expander("Full latest event"):
            st.json(latest)

    st.markdown("---")
    st.header("Accepted Trajectory")

    state_dict = runtime.to_dict()

    accepted = state_dict["accepted_trajectory"]
    rejected = state_dict["rejected_inputs"]

    if accepted:
        for index, turn in enumerate(accepted, start=1):
            with st.expander(f"Accepted {index}: {turn['text'][:60]}"):
                st.write(turn["text"])
                st.json(turn["measurements"]["summary"])
    else:
        st.write("No accepted turns yet.")

    st.header("Rejected Inputs")

    if rejected:
        for index, turn in enumerate(rejected, start=1):
            with st.expander(f"Rejected {index}: {turn['state']}"):
                st.write(turn["text"])
                st.write("Reason:", turn["reason"])
                st.json(turn["measurements"]["summary"])
    else:
        st.write("No rejected inputs yet.")