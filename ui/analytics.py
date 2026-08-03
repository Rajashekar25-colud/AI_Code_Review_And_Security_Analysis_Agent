import streamlit as st


def render_analytics_page(review_result):
    """
    Analytics page for AI Code Review Agent.
    Displays charts and metrics generated from the latest review.
    """

    st.title("📊 Analytics Dashboard")

    if review_result is None:

        st.info(
            "No analysis available.\n\n"
            "Run a code review from **New Review** to view analytics."
        )

        return

    # Import here to avoid importing heavy dependencies (e.g. pandas)
    # at app startup when the analytics/dashboard pages are not used.
    from ui.dashboard import render_dashboard

    render_dashboard(review_result)