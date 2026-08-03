import os

import streamlit as st
from dotenv import load_dotenv


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Import Application Modules
# ==========================================================

from agents.orchestrator import Orchestrator

from ui.sidebar import render_sidebar
from ui.review_page import render_review_page
from ui.analytics import render_analytics_page
from ui.report_page import render_report_page
from ui.assistant import render_assistant_page
from ui.history import render_history_page
from ui.settings import render_settings_page



# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(

    page_title="AI Code Review & Security Analysis Agent",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)



# ==========================================================
# Load Custom CSS
# ==========================================================

css_file = os.getenv(
    "CSS_PATH",
    "assets/css.css"
)


if os.path.exists(css_file):

    with open(
        css_file,
        "r",
        encoding="utf-8"
    ) as file:

        st.markdown(

            f"<style>{file.read()}</style>",

            unsafe_allow_html=True

        )



# ==========================================================
# Session State Initialization
# ==========================================================

if "orchestrator" not in st.session_state:

    st.session_state.orchestrator = Orchestrator()



if "review_result" not in st.session_state:

    st.session_state.review_result = None



if "history" not in st.session_state:

    st.session_state.history = []



if "chat_history" not in st.session_state:

    st.session_state.chat_history = []



# ==========================================================
# Sidebar Navigation
# ==========================================================

page = render_sidebar()



# ==========================================================
# Page Routing
# ==========================================================

if page == "📝 New Review":


    render_review_page(

        st.session_state.orchestrator

    )


elif page == "📊 Analytics":


    render_analytics_page(

        st.session_state.review_result

    )


elif page == "📄 Reports":


    render_report_page(

        st.session_state.review_result

    )


elif page == "🤖 AI Assistant":


    render_assistant_page(

        st.session_state.review_result

    )


elif page == "🕘 History":


    render_history_page()



elif page == "⚙ Settings":


    render_settings_page()



# ==========================================================
# Footer
# ==========================================================

st.divider()


col1, col2, col3 = st.columns(3)


with col1:

    st.caption(
        "AI Code Review & Security Analysis Agent"
    )


with col2:

    st.caption(
        "Multi-Agent Secure Coding Platform"
    )


with col3:

    st.caption(
        "Python • Java • LangGraph • Groq • RAG"
    )