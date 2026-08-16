import os
import logging

import streamlit as st
from dotenv import load_dotenv


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Logging
# ==========================================================

from config import APPLICATION_LOG_FILE, LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(APPLICATION_LOG_FILE),
        logging.StreamHandler()
    ]
)


# ==========================================================
# Database Setup (must run before anything touches the DB)
# ==========================================================

from database.migrations import run_migrations

run_migrations()


# ==========================================================
# Import Application Modules
# ==========================================================

from agents.orchestrator import Orchestrator

from database.auth import get_user_by_session, delete_session

from ui.login import render_login_page
from ui.signup import render_signup_page
from ui.sidebar import render_sidebar
from ui.review_page import render_review_page
from ui.report_page import render_report_page
from ui.history import render_history_page
from ui.settings import render_settings_page


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Smart Code Inspection Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# Load Custom CSS
# ==========================================================

css_file = os.getenv("CSS_PATH", "assets/css.css")

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


# ==========================================================
# Session State Initialization
# ==========================================================

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()

if "review_result" not in st.session_state:
    st.session_state.review_result = None

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"


# ==========================================================
# Restore login from URL session token (survives page refresh)
# ==========================================================

if st.session_state.user is None:

    token = st.query_params.get("session")

    if token:

        restored_user = get_user_by_session(token)

        if restored_user:
            st.session_state.user = restored_user


# ==========================================================
# Auth Gate - nothing below runs until logged in
# ==========================================================

if st.session_state.user is None:

    if st.session_state.auth_page == "signup":
        render_signup_page()
    else:
        render_login_page()

    st.stop()


# ==========================================================
# Sidebar Navigation
# ==========================================================

page = render_sidebar()

# Force routing to a specific page when another page (e.g.
# History's "Restore" button) requested it - guaranteed to work
# regardless of how the sidebar radio widget itself behaves.
if "force_page" in st.session_state:
    page = st.session_state.pop("force_page")


# ==========================================================
# Page Routing
# ==========================================================

if page == "📝 New Review":

    render_review_page(st.session_state.orchestrator)

elif page == "📄 Reports":

    render_report_page(st.session_state.review_result)

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
    st.caption("Smart Code Inspection Platform")

with col2:
    st.caption("Vulnerability Detection System - Multi-Agent Pipeline")

with col3:
    st.caption("Python • Java • LangGraph • Groq • RAG")