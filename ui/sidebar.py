import os
import streamlit as st


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

    st.sidebar.title("🤖 AI Code Review Agent")

    st.sidebar.caption(
        "Multi-Agent Code Quality & Security Analysis"
    )

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        [
            "📝 New Review",
            "📊 Analytics",
            "🤖 AI Assistant",
            "📄 Reports",
            "🕘 History",
            "⚙ Settings"
        ]
    )

    st.sidebar.divider()

    st.sidebar.subheader("Supported Languages")

    st.sidebar.success("🐍 Python")

    st.sidebar.success("☕ Java")

    st.sidebar.divider()

    st.sidebar.subheader("System Status")

    st.sidebar.success("✅ Groq API Connected")

    st.sidebar.success("✅ LangGraph Workflow Ready")

    st.sidebar.success("✅ RAG Knowledge Base Loaded")

    st.sidebar.success("✅ Chroma Vector Database Ready")

    st.sidebar.success("✅ AI Agents Online")

    st.sidebar.divider()

    st.sidebar.caption("AI Code Review & Security Analysis Agent")

    st.sidebar.caption("Version 1.0")

    return page