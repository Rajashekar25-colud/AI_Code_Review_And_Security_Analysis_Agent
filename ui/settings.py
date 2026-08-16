import os
import streamlit as st

from database.repository import get_history, delete_review
from database.repository import get_chat_history, delete_chat_history


def render_settings_page():
    """
    Application settings page.
    """

    st.title("⚙ Settings")

    user = st.session_state.get("user")

    st.subheader("Application")

    st.write("**Project:** Smart Code Inspection Platform with Vulnerability Detection System")
    st.write("**Version:** 1.0")
    st.write("**Framework:** Streamlit")
    st.write("**Workflow:** LangGraph")

    if user:
        st.write(f"**Logged in as:** {user['email']}")

    st.divider()

    st.subheader("LLM Configuration")

    groq_key = os.getenv("GROQ_API_KEY")

    if groq_key:
        st.success("Groq API Key Configured")
    else:
        st.error("Groq API Key Not Found")

    st.divider()

    st.subheader("Knowledge Base")

    if os.path.exists("chroma_db"):
        st.success("Chroma Vector Database Available")
    else:
        st.warning("Knowledge Base Not Built")

    if os.path.exists("knowledge_base"):
        st.success("Knowledge Base Documents Found")
    else:
        st.warning("Knowledge Base Folder Missing")

    st.divider()

    st.subheader("Supported Languages")

    st.markdown(
        """
- Python
- Java
"""
    )

    st.divider()

    st.subheader("Installed Analysis Tools")

    tools = {
        "Pylint": True,
        "Radon": True,
        "Bandit": True,
        "PMD": os.path.exists("tools/pmd-bin-7.26.0"),
        "Checkstyle": os.path.exists("tools/checkstyle-13.9.0-all.jar"),
        "SpotBugs": os.path.exists("tools/spotbugs-4.10.3")
    }

    for tool, available in tools.items():

        if available:
            st.success(f"{tool} ✓")
        else:
            st.warning(f"{tool} Not Found")

    st.divider()

    st.subheader("Environment")

    st.write(f"**Current Working Directory:** `{os.getcwd()}`")
    st.write(f"**Python Version:** `{os.sys.version.split()[0]}`")

    st.divider()

    st.subheader("Data")

    if not user:

        st.info("Log in to manage your saved reviews and chat history.")
        return

    reviews = get_history(user["id"])

    st.write(f"**Saved Reviews:** {len(reviews)}")

    total_chat_messages = 0

    for review in reviews:
        total_chat_messages += len(get_chat_history(review["id"]))

    st.write(f"**Saved Chat Messages:** {total_chat_messages}")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Clear All Chat History", width="stretch"):

            for review in reviews:
                delete_chat_history(review["id"])

            st.session_state.chat_threads = {}
            st.success("All chat history cleared from the database.")
            st.rerun()

    with col2:

        if st.button("Clear All Review History", width="stretch"):

            for review in reviews:
                delete_review(review["id"])

            st.session_state.review_result = None
            st.session_state.active_review_id = None
            st.success("All reviews deleted from the database.")
            st.rerun()