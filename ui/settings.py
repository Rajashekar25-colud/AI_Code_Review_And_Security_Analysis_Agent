import os
import streamlit as st


def render_settings_page():
    """
    Application settings page.
    """

    st.title("⚙ Settings")

    st.subheader("Application")

    st.write("**Project:** AI Code Review & Security Analysis Agent")
    st.write("**Version:** 1.0")
    st.write("**Framework:** Streamlit")
    st.write("**Workflow:** LangGraph")

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

    if st.button(
        "Clear Chat History",
        width="stretch"
    ):

        st.session_state["chat_history"] = []

        st.success("Chat history cleared.")

    if st.button(
        "Clear Review History",
        width="stretch"
    ):

        st.session_state["history"] = []

        st.success("Review history cleared.")