"""
Central application configuration.

Single place for paths, environment variable names, and default
values — so nothing else in the codebase hardcodes a path or an
env var name directly.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = os.path.join(BASE_DIR, "config")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

CSS_PATH = os.getenv("CSS_PATH", os.path.join(BASE_DIR, "assets", "css.css"))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")


# ==========================================================
# Database
# ==========================================================

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    os.path.join(BASE_DIR, "app_data.db")
)


# ==========================================================
# LLM / Groq
# ==========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")


# ==========================================================
# Static Analysis Tool Paths
# ==========================================================

PMD_PATH = os.getenv(
    "PMD_PATH",
    os.path.join(BASE_DIR, "tools", "pmd-bin-7.26.0", "bin", "pmd")
)

CHECKSTYLE_JAR_PATH = os.getenv(
    "CHECKSTYLE_JAR_PATH",
    os.path.join(BASE_DIR, "tools", "checkstyle-13.9.0-all.jar")
)

SPOTBUGS_PATH = os.getenv(
    "SPOTBUGS_PATH",
    os.path.join(BASE_DIR, "tools", "spotbugs-4.10.3", "bin", "spotbugs")
)


# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APPLICATION_LOG_FILE = os.path.join(LOGS_DIR, "application.log")


# ==========================================================
# Ensure required directories exist at import time
# ==========================================================

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)