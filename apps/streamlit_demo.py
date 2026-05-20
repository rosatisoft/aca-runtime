import streamlit as st

from aca_runtime.runtime.supervision_modes import supervise_message


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"


st.set_page_config(
    page_title="ACA Runtime Supervision Demo",
    layout="wide",
)

st.title("ACA Runtime — Supervised Chat Demo")

if "history" not in st.session_state:
    st.session_state.history = []

if "events" not in st.session_state:
    st.session_state.events = []

mode = st.sidebar.selectbox(
    "Supervision Mode",
    ["report", "warning", "interactive", "moderator"],
)

st.sidebar.markdown("---")
st.sidebar.write("Current mode:", mode)

left, right = st.columns([2, 1])

with left:
    st.header("Chat")

    for event in st.session_state.events:
        st.chat_message("user").write(event["user_message"])

        intervention = event["intervention"]

        if mode == "report":
            st.chat_message("assistant").write(
                "Message received. ACA is reporting silently."
            )

        elif intervention["should_intervene"]:
            st.chat_message("assistant").write(
                intervention["message"]
            )

        else:
            st.chat_message("assistant").write(
                "Proceeding normally. No intervention required."
            )

    user_input = st.chat_input("Write a message...")

    if user_input:
        result = supervise_message(
            user_message=user_input,
            history=st.session_state.history,
            artifacts_path=ARTIFACTS_PATH,
            mode=mode,
        )

        st.session_state.history = result["history"]
        st.session_state.events.append(result)

        st.rerun()

with right:
    st.header("ACA Orientation Panel")

    if st.session_state.events:
        latest = st.session_state.events[-1]

        runtime = latest["runtime"]
        trajectory = latest["trajectory"]
        intervention = latest["intervention"]

        # Status banner
        if trajectory["drift_detected"] or "DRIFT" in runtime["decision"]:
            st.error("🔴 Drift detected")
        elif runtime["ambiguity"] == "AMBIGUOUS" or "CLARIFY" in runtime["decision"]:
            st.warning("🟡 Ambiguous / clarification recommended")
        else:
            st.success("🟢 Stable orientation")

        st.subheader("Runtime")
        st.metric("Decision", runtime["decision"])
        st.metric("Semantic Field", runtime["semantic_field"])
        st.metric("Origin Cost", round(runtime["origin_cost"], 4))
        st.metric("Criterion Confidence", round(runtime["criterion_confidence"], 4))

        st.subheader("Trajectory")
        st.metric("Status", trajectory["trajectory_status"])
        st.metric("Drift Detected", str(trajectory["drift_detected"]))
        st.metric("Preservation", round(trajectory["criterion_preservation"], 4))
        st.metric("Entropy", round(trajectory["trajectory_entropy"], 4))

        st.subheader("Criterion Preservation")

        preservation = trajectory["criterion_preservation"]
        st.progress(preservation)

        if preservation >= 0.75:
            st.success("High preservation")
        elif preservation >= 0.50:
            st.warning("Moderate preservation")
        else:
            st.error("Low preservation")

        st.subheader("Criterion Path")

        path = trajectory["field_sequence"]

        if path:
            st.code(
                "\n↓\n".join(path)
            )

        st.subheader("Last Criterion Event")

        drift_events = trajectory["drift_events"]

        if drift_events:
            st.warning(drift_events[-1])
        else:
            st.success("No drift events detected.")

        st.subheader("Intervention")
        st.write("Level:", intervention["level"])
        st.write("Action:", intervention["action"])
        st.write("Message:", intervention["message"])

        st.subheader("Guidance")
        for item in latest["criterion_response"]["response_guidance"]:
            st.write("-", item)

    else:
        st.info("Start the chat to see ACA orientation signals.")