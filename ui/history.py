import streamlit as st

from database.repository import get_history, delete_review, get_review_by_id


def render_history_page():
    """
    Display previous code reviews for the logged-in user, pulled
    from the database instead of session state. Each entry can be
    restored (loads it back into st.session_state.review_result and
    jumps straight to the New Review page, since that's where the
    dashboard and embedded chat live) or deleted.
    """

    st.title("🕘 Review History")

    user = st.session_state.get("user")

    if not user:
        st.info("Please log in to view your review history.")
        return

    reviews = get_history(user["id"])

    if not reviews:
        st.info(
            "No review history available.\n\n"
            "Run a code review to create history."
        )
        return

    for review in reviews:

        findings = review.get("findings", [])
        total = len(findings)
        language = review.get("language", "Unknown")
        filename = review.get("filename") or "Untitled review"
        score = review.get("overall_score", 0)
        created_at = review.get("created_at", "")

        with st.expander(
            f"{filename} • {language} • {total} finding(s) • "
            f"Score {score} • {created_at}"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Overall Score", score)

            with col2:
                st.metric("Findings", total)

            with col3:
                st.write("")
                st.write("")
                if st.button(
                    "🔄 Restore",
                    key=f"restore_{review['id']}",
                    width="stretch"
                ):
                    restored = get_review_by_id(review["id"])

                    st.session_state.review_result = {
                        "filename": restored.get("filename"),
                        "language": restored.get("language"),
                        "findings": restored.get("findings", []),
                        "pr_summary": restored.get("summary", ""),
                        "remediation": {},
                        "lines": 0
                    }
                    st.session_state.active_review_id = restored["id"]

                    # Jump straight to New Review, where the
                    # dashboard and embedded chat actually render.
                    st.session_state.nav_override = "📝 New Review"
                    st.session_state.force_page = "📝 New Review"

                    st.rerun()

            if findings:

                for finding in findings:

                    severity = str(finding.get("severity", "LOW")).upper()
                    issue = finding.get("type") or finding.get("category") or "Finding"
                    description = finding.get("description", "No description.")
                    recommendation = finding.get("recommendation", "No recommendation.")

                    st.markdown(f"**{severity} • {issue}**")
                    st.write(description)
                    st.caption(f"Recommendation: {recommendation}")
                    st.divider()

            else:
                st.success("No issues were found in this review.")

            if st.button(
                "🗑 Delete this review",
                key=f"delete_{review['id']}"
            ):
                delete_review(review["id"])
                st.rerun()