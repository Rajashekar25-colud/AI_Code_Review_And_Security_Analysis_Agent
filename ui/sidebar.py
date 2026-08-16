import os
import streamlit as st

from database.repository import get_history
from database.auth import delete_session


def render_sidebar():
    """
    Render the application sidebar.

    Returns
    -------
    str
        Selected navigation page.
    """

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        st.sidebar.image(
            logo_path,
            width="stretch"
        )

    st.sidebar.title("🤖 Smart Code Inspection Platform")

    st.sidebar.caption(
        "Vulnerability Detection System"
    )

    st.sidebar.divider()

    nav_options = [
        "📝 New Review",
        "📄 Reports",
        "🕘 History",
        "⚙ Settings"
    ]

    # ------------------------------------------------------
    # Allow other pages (e.g. History's "Restore" button) to
    # force the sidebar to jump to a specific page. They do
    # this by setting st.session_state.nav_override before
    # calling st.rerun() - we apply it here, once, before the
    # radio widget is created.
    # ------------------------------------------------------

    if "nav_override" in st.session_state:

        st.session_state["nav_radio"] = st.session_state.pop("nav_override")

    page = st.sidebar.radio(
        "Navigation",
        nav_options,
        key="nav_radio"
    )

    user = st.session_state.get("user")

    if user:

        st.sidebar.divider()
        st.sidebar.subheader("Recent Reviews")

        reviews = get_history(user["id"])[:5]

        if reviews:

            for review in reviews:

                filename = review.get("filename") or "Untitled"
                score = review.get("overall_score", 0)

                st.sidebar.caption(f"{filename} — {score}")

        else:
            st.sidebar.caption("No reviews yet.")

    st.sidebar.divider()

    st.sidebar.subheader("Supported Languages")

    st.sidebar.success("🐍 Python")
    st.sidebar.success("☕ Java")

    st.sidebar.divider()

    if user:
        st.sidebar.caption(f"👤 {user.get('name') or user['email']}")

        if st.sidebar.button("Logout", width="stretch"):

            token = st.query_params.get("session")

            if token:
                delete_session(token)

            st.query_params.clear()

            st.session_state.user = None
            st.session_state.review_result = None
            st.rerun()

    st.sidebar.divider()

    st.sidebar.caption("Smart Code Inspection Platform")
    st.sidebar.caption("Version 1.0")

    return page