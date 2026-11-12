
import streamlit as st

from sysmedic import analyse_linux_issue
from knowledge_base import (
    initialise_database,
    save_case,
    get_approved_cases
)

APP_NAME = "KernelX — SysMedic"
MAX_LOG_CHARS = 20000

initialise_database()

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🖥️",
    layout="wide"
)

st.title("🖥️ KernelX")
st.subheader("SysMedic — Linux Doctor")

st.caption(
    "Independent Linux troubleshooting engine for "
    "infrastructure engineers and IT service providers."
)

with st.sidebar:
    st.header("SysMedic")
    st.success("Local diagnostic engine active")
    st.caption("AI provider: None")
    st.caption("External API: Not required")
    st.caption("Knowledge base: SQLite")

    st.divider()

    st.markdown("### Privacy and Safety")
    st.caption(
        "Remove passwords, tokens, private keys and "
        "customer-sensitive information before submitting data."
    )
    st.caption(
        "SysMedic recommends commands only. "
        "It never executes commands on your servers."
    )

st.divider()

st.markdown("### Describe your Linux problem")

incident = st.text_area(
    "What happened?",
    placeholder=(
        "Example: The server is unable to resolve "
        "example.com. The error says Temporary failure "
        "in name resolution."
    ),
    height=150
)

environment = st.selectbox(
    "Environment",
    ["Development / Test", "Staging", "Production"]
)

issue_category = st.selectbox(
    "Problem category",
    [
        "Network / DNS",
        "Service failure",
        "Disk / Filesystem",
        "CPU / Memory",
        "Permissions",
        "Boot issue",
        "Process issue",
        "Other"
    ]
)

uploaded = st.file_uploader(
    "Upload diagnostic logs (optional)",
    type=["txt", "log", "out"]
)

log_text = ""

if uploaded is not None:
    log_text = uploaded.getvalue().decode(
        "utf-8",
        errors="replace"
    )

    if len(log_text) > MAX_LOG_CHARS:
        st.warning(
            "Only the first 20,000 characters will be analysed."
        )
        log_text = log_text[:MAX_LOG_CHARS]

    st.caption(f"Loaded {len(log_text):,} characters.")

st.divider()

if st.button(
    "Diagnose with SysMedic",
    type="primary",
    use_container_width=True
):

    if not incident.strip() and not log_text.strip():
        st.error("Please describe an issue or upload a log.")

    else:
        diagnostic_input = f"""
Environment: {environment}
Problem category: {issue_category}

Problem description:
{incident}

Diagnostic logs:
{log_text}
"""

        try:
            with st.spinner("SysMedic is investigating..."):
                diagnosis = analyse_linux_issue(diagnostic_input)

            st.session_state["latest_diagnosis"] = diagnosis
            st.session_state["latest_incident"] = incident
            st.session_state["latest_category"] = issue_category
            st.session_state["latest_environment"] = environment
            st.session_state["feedback_saved"] = False

        except Exception as exc:
            st.error("SysMedic encountered an error.")
            st.code(str(exc))

if "latest_diagnosis" in st.session_state:

    st.success("Diagnosis generated.")

    st.markdown("## SysMedic Diagnosis")
    st.markdown(st.session_state["latest_diagnosis"])

    st.info(
        "These are diagnostic recommendations only. "
        "No commands have been executed."
    )

    st.divider()

    st.markdown("## Previous troubleshooting knowledge")

    previous_cases = get_approved_cases(
        category=st.session_state["latest_category"]
    )

    if previous_cases:
        st.caption(
            f"Found {len(previous_cases)} approved previous "
            "case(s) in this category."
        )

        for case in previous_cases[:5]:
            with st.expander(
                f"Previous case #{case['id']}"
            ):
                st.write("**Symptoms:**")
                st.write(case["symptoms"])

                st.write("**Confirmed root cause:**")
                st.write(case["root_cause"])

                st.write("**Recorded resolution:**")
                st.write(case["resolution"])

                st.caption(
                    "Historical case, not a verified diagnosis "
                    "of the current incident."
                )
    else:
        st.info(
            "No approved historical cases in this category yet. "
            "SysMedic can build this knowledge as engineers "
            "submit reviewed resolutions."
        )

    st.divider()

    st.markdown("## Help SysMedic learn")

    st.write(
        "After investigating the issue, record what actually "
        "happened. This feedback will help build the local "
        "troubleshooting knowledge base."
    )

    with st.form("resolution_feedback"):

        actual_root_cause = st.text_area(
            "What was the actual root cause?",
            placeholder="Describe the confirmed cause..."
        )

        actual_resolution = st.text_area(
            "How was the issue resolved?",
            placeholder="Describe the steps that resolved it..."
        )

        resolution_success = st.radio(
            "Was the issue successfully resolved?",
            ["Yes", "No", "Still investigating"],
            horizontal=True
        )

        approve_reuse = st.checkbox(
            "I have removed sensitive information and approve "
            "this case for reuse in future recommendations."
        )

        submitted = st.form_submit_button(
            "Save troubleshooting feedback",
            use_container_width=True
        )

        if submitted:

            if not actual_root_cause.strip():
                st.error("Please enter the actual root cause.")

            elif not actual_resolution.strip():
                st.error("Please enter the resolution details.")

            elif st.session_state["feedback_saved"]:
                st.warning(
                    "Feedback has already been saved for this diagnosis."
                )

            else:
                try:
                    save_case(
                        category=st.session_state["latest_category"],
                        symptoms=st.session_state["latest_incident"],
                        root_cause=actual_root_cause,
                        resolution=actual_resolution,
                        successful=(resolution_success == "Yes"),
                        approved_for_reuse=approve_reuse
                    )

                    st.session_state["feedback_saved"] = True

                    st.success(
                        "Feedback saved successfully to the "
                        "local SysMedic knowledge base."
                    )

                    if approve_reuse:
                        st.success(
                            "This reviewed case is now approved "
                            "for future recommendations."
                        )
                    else:
                        st.info(
                            "This case is stored locally but "
                            "will not be reused in future diagnoses."
                        )

                except Exception as exc:
                    st.error("Unable to save feedback.")
                    st.code(str(exc))

st.divider()

st.caption("KernelX | SysMedic | Prototype v0.3")
