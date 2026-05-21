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

        declared_shift = latest.get(
            "declared_shift",
            {}
        )

        runtime = latest["runtime"]
        trajectory = latest["trajectory"]
        intervention = latest["intervention"]

        # Status banner
        is_recovering = (
            declared_shift.get("declared_shift")
            and trajectory["drift_detected"]
        )

        if is_recovering:
            st.warning("🟡 Recovering orientation")
        elif trajectory["drift_detected"] or "DRIFT" in runtime["decision"]:
            st.error("🔴 Drift detected")
        elif runtime["ambiguity"] == "AMBIGUOUS" or "CLARIFY" in runtime["decision"]:
            st.warning("🟡 Ambiguous / clarification recommended")
        else:
            st.success("🟢 Stable orientation")

        st.subheader("Runtime")
        decision = runtime["decision"]

        if is_recovering:
            decision = "RECOVERING"

        st.metric(
            "Decision",
            decision
        )
        st.metric("Semantic Field", runtime["semantic_field"])
        st.metric("Origin Cost", round(runtime["origin_cost"], 4))
        st.metric("Criterion Confidence", round(runtime["criterion_confidence"], 4))

        st.subheader("Trajectory")

        trajectory_status = trajectory["trajectory_status"]

        if is_recovering:
            trajectory_status = "recovering"

        st.metric("Status", trajectory_status)
        st.metric("Drift Detected", str(trajectory["drift_detected"]))
        st.metric("Preservation", round(trajectory["criterion_preservation"], 4))
        st.metric("Entropy", round(trajectory["trajectory_entropy"], 4))
        st.subheader("Declared Shift")

        st.metric(
            "Detected",
            str(
                declared_shift.get(
                    "declared_shift",
                    False,
                )
            ),
        )

        if declared_shift.get("declared_shift"):

            st.write(
                "Type:",
                declared_shift["shift_type"]
            )

            st.write(
                "Evidence:",
                declared_shift["evidence"]
            )

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

        st.subheader("Interpretation")

        interpretation = []

        if is_recovering:

            interpretation.append(
                "Conversation returned through an explicit criterion transition, "
                "but recovery is not yet complete."
            )

        elif trajectory["drift_detected"]:

            if declared_shift.get("declared_shift"):

                interpretation.append(
                    "Conversation changed orientation through a declared frame transition."
                )

            else:

                interpretation.append(
                    "Conversation moved away from the previous criterion without declaring a new frame."
                )

        elif runtime["ambiguity"] == "AMBIGUOUS":

            interpretation.append(
                "The current message can be interpreted under multiple nearby frames."
            )

        else:

            interpretation.append(
                "The conversation remains sufficiently aligned with the current criterion."
            )

        for item in interpretation:
            st.info(item)

        st.subheader("Operational Meaning")

        meaning = []

        if is_recovering:

            meaning.append(
                "A declared criterion recovery was detected. Continue operating under the "
                "new frame and observe whether preservation stabilizes."
            )

        elif trajectory["drift_detected"]:

            meaning.append(
                "Consider clarifying whether a new criterion or frame was introduced."
            )

        if declared_shift.get("declared_shift") and not is_recovering:

            meaning.append(
                "Interpret the next messages using the newly declared frame."
            )

        if not meaning:

            meaning.append(
                "No criterion intervention recommended."
            )

        for item in meaning:
            st.success(item)

        st.subheader("Intervention")
        st.write("Level:", intervention["level"])
        st.write("Action:", intervention["action"])
        st.write("Message:", intervention["message"])

        st.subheader("Guidance")
        for item in latest["criterion_response"]["response_guidance"]:
            st.write("-", item)

    else:
        st.info("Start the chat to see ACA orientation signals.")