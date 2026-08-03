import streamlit as st


def render_history_page():
    """
    Display previous code review history.
    """

    st.title("🕘 Review History")

    history = st.session_state.get("history", [])

    if not history:

        st.info(
            "No review history available.\n\n"
            "Run a code review to create history."
        )

        return

    for index, review in enumerate(
        reversed(history),
        start=1
    ):

        language = review.get(
            "language",
            "Unknown"
        )

        findings = review.get(
            "findings",
            []
        )

        total = len(findings)

        with st.expander(
            f"Review {index} • {language} • {total} Finding(s)"
        ):

            st.write(
                f"**Language:** {language}"
            )

            st.write(
                f"**Total Findings:** {total}"
            )

            if findings:

                for finding in findings:

                    severity = finding.get(
                        "severity",
                        "LOW"
                    )

                    issue = finding.get(
                        "type",
                        "Unknown Issue"
                    )

                    description = finding.get(
                        "description",
                        "No description."
                    )

                    recommendation = finding.get(
                        "recommendation",
                        "No recommendation."
                    )

                    st.markdown(
                        f"### {severity} • {issue}"
                    )

                    st.write(description)

                    st.caption(
                        f"Recommendation: {recommendation}"
                    )

                    st.divider()

            else:

                st.success(
                    "No issues were found in this review."
                )