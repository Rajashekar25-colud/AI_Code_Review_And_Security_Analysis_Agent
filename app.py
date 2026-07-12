import streamlit as st

from modules.syntax_validator import validate_code
from modules.language_detector import detect_language
from rag.build_knowledgebase import build_knowledge_base


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🤖 AI Reviewer")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 New Review",
        "📚 Knowledge Base",
        "📄 Reports",
        "🕘 History",
        "⚙ Settings"
    ]
)

st.sidebar.divider()

st.sidebar.write("### Supported Languages")
st.sidebar.write("✔ Python")
st.sidebar.write("✔ Java")

st.sidebar.divider()




# ======================================================
# NEW REVIEW
# ======================================================

if page == "🏠 New Review":

    st.title("AI Code Review & Security Analysis Agent")

    st.write(
        "Upload a Java or Python file or paste your source code below."
    )

    st.divider()

    left, right = st.columns([2, 1])

    # -----------------------------
    # Left Side
    # -----------------------------

    with left:

        st.subheader("Source Code")

        uploaded_file = st.file_uploader(
            "Upload Java or Python File",
            type=["py", "java"]
        )

        st.write("OR")

        code = st.text_area(
            "Paste your code here",
            height=350,
            placeholder="Paste Java or Python source code..."
        )

    # -----------------------------
    # Right Side
    # -----------------------------

    with right:

        st.subheader("Options")

        language = st.selectbox(
            "Programming Language",
            [
                "Auto Detect",
                "Python",
                "Java"
            ]
        )

        analyze = st.button(
            "Analyze Code",
            use_container_width=True
        )

        st.info(
            """
**Analysis includes**

- Syntax Validation
- Language Detection
- Secure Code Review
- Code Quality Analysis
"""
        )

    # -----------------------------
    # Analyze
    # -----------------------------

    if analyze:

        if uploaded_file is None and code.strip() == "":

            st.error("Please upload a file or paste code.")

        else:

            # Read Code

            if uploaded_file is not None:

                source_code = uploaded_file.read().decode("utf-8")

                file_name = uploaded_file.name

            else:

                source_code = code

                file_name = "Pasted Code"

            # Language Detection

            if language == "Auto Detect":

                if uploaded_file is not None:

                    language = detect_language(file_name)

                else:

                    # Detect from code
                    language = detect_language(source_code)

            # Syntax Validation

            valid, message = validate_code(
                source_code,
                language
            )

            # Results

            st.divider()

            st.subheader("Analysis Result")

            st.write("**File Name :**", file_name)

            st.write("**Language :**", language)

            st.write(
                "**Total Lines :**",
                len(source_code.splitlines())
            )

            if valid:

                st.success(message)

                st.success(
                    "Status : Ready for Security Analysis"
                )

            else:

                st.error(message)


# ======================================================
# KNOWLEDGE BASE
# ======================================================

elif page == "📚 Knowledge Base":

    st.title("Secure Coding Knowledge Base")

    st.write("The following documents are indexed.")

    st.write("• OWASP Top 10")

    st.write("• Java Secure Coding")

    st.write("• Python Secure Coding")

    st.write("• Secure Coding Guidelines")

    st.divider()

    if st.button(
        "Build Knowledge Base",
        use_container_width=True
    ):

        with st.spinner(
            "Building Knowledge Base..."
        ):

            try:

                result = build_knowledge_base()

                st.success(result)

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


# ======================================================
# REPORTS
# ======================================================

elif page == "📄 Reports":

    st.title("Reports")

    st.info(
        "Generated reports will appear here."
    )


# ======================================================
# HISTORY
# ======================================================

elif page == "🕘 History":

    st.title("History")

    st.info(
        "Previous code reviews will appear here."
    )


# ======================================================
# SETTINGS
# ======================================================

elif page == "⚙ Settings":

    st.title("Settings")

    theme = st.selectbox(
        "Theme",
        [
            "Dark",
            "Light"
        ]
    )

    notifications = st.checkbox(
        "Enable Notifications"
    )

    st.success("Settings Saved")


# ======================================================
# Footer
# ======================================================

st.divider()

st.caption(
    "AI Code Review & Security Analysis Agent"
)