import streamlit as st

from aca_runtime.runtime.supervision_modes import supervise_message


ARTIFACTS_PATH = r"C:\Users\ernes\documents\aca\artifacts"

def build_moderator_decision(result: dict) -> dict:
    runtime = result["runtime"]
    trajectory = result.get("trajectory", {})

    trajectory_status = trajectory.get(
        "status",
        "unknown"
    )

    drift_detected = trajectory.get(
        "drift_detected",
        False
    )
    declared_shift = result.get("declared_shift", {})

    decision = runtime["decision"]
    field = runtime["semantic_field"]
    origin_cost = runtime["origin_cost"]
    ambiguity = runtime["ambiguity"]

    is_recovering = (
        declared_shift.get("declared_shift")
        and drift_detected
    )

    if is_recovering:
        return {
            "action": "RECOVER",
            "label": "Recovering criterion",
            "message": (
                "ACA detected a declared return toward the active criterion. "
                "Continue under the recovered frame and keep conclusions supported."
            ),
        }

    if origin_cost >= 0.88 and field == "rhetorical":
        return {
            "action": "FLAG_ABSURD_OR_UNSUPPORTED",
            "label": "Unsupported or absurd framing",
            "message": (
                "ACA detected a highly unstable or unsupported framing. "
                "Please restate the claim in measurable or evidence-based terms."
            ),
        }

    if ambiguity == "AMBIGUOUS" or "CLARIFY" in decision:
        return {
            "action": "CLARIFY",
            "label": "Clarification required",
            "message": (
                "ACA detected ambiguity. Please clarify the intended frame: "
                "factual, hypothetical, rhetorical, or exploratory."
            ),
        }

    if (
        drift_detected
        and trajectory_status != "stable"
    ):
        return {
            "action": "REANCHOR",
            "label": "Criterion drift detected",
            "message": (
                "ACA detected movement away from the active criterion. "
                "Re-anchor the discussion before continuing."
            ),
        }

    return {
        "action": "ANSWER",
        "label": "Stable criterion",
        "message": (
            "ACA detected sufficient stability. Proceed with a clear and concise answer."
        ),
    }


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

        elif mode == "interactive":
            moderator_decision = build_moderator_decision(event)

            st.chat_message("assistant").write(
                f"{moderator_decision['label']}: "
                f"{moderator_decision['message']}"
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
        trajectory = latest.get(
            "trajectory",
            {}
        )

        trajectory_status = trajectory.get(
            "trajectory_status",
            trajectory.get(
                "status",
                "unknown"
            )
        )
        intervention = latest["intervention"]

        # Status banner
        is_recovering = (
            declared_shift.get("declared_shift")
            and trajectory.get(
                "drift_detected",
                False
            )
        )

        if is_recovering:
            st.warning("🟡 Recovering orientation")
        elif trajectory.get("drift_detected", False):
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

        trajectory_status = trajectory.get(
            "trajectory_status",
            trajectory.get(
                "status",
                "unknown"
            )
        )

        if is_recovering:
            trajectory_status = "recovering"

        st.metric("Status", trajectory_status)
        st.metric("Drift Detected", str(trajectory.get("drift_detected", False)))
        st.metric("Preservation", round(trajectory.get("criterion_preservation", 0.0), 4))
        st.metric("Entropy", round(trajectory.get("trajectory_entropy", 0.0), 4))
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

        preservation = trajectory.get("criterion_preservation", 0.0)
        st.progress(preservation)

        if preservation >= 0.75:
            st.success("High preservation")
        elif preservation >= 0.50:
            st.warning("Moderate preservation")
        else:
            st.error("Low preservation")

        st.subheader("Criterion Path")

        path = trajectory.get("field_sequence",[])

        if path:
            st.code(
                "\n↓\n".join(path)
            )

        st.subheader("Last Criterion Event")

        drift_events = trajectory.get("drift_events", [])

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

        elif trajectory.get(
            "drift_detected",
            False
        ):

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

        elif trajectory.get("drift_detected", False):

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

        st.subheader("Operational Decision")

        if mode == "interactive":
            moderator_decision = build_moderator_decision(latest)

            st.subheader("Moderator Decision")
            st.write("Action:", moderator_decision["action"])
            st.write("Label:", moderator_decision["label"])
            st.write("Message:", moderator_decision["message"])

        else:
            st.write("Level:", intervention["level"])
            st.write("Action:", intervention["action"])
            st.write("Message:", intervention["message"])

        st.subheader("Guidance")
        for item in latest["criterion_response"]["response_guidance"]:
            st.write("-", item)

    else:
        st.info("Start the chat to see ACA orientation signals.")