import streamlit as st

from modules.syntax_validator import validate_code
from modules.language_detector import detect_language

from rag.build_knowledgebase import build_knowledge_base

from agents.orchestrator import Orchestrator


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🤖",
    layout="wide"
)


# Create Orchestrator

orchestrator = Orchestrator()



# =====================================================
# Sidebar
# =====================================================

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


st.sidebar.markdown(
    "### Supported Languages"
)


st.sidebar.success(
    "Python"
)


st.sidebar.success(
    "Java"
)


st.sidebar.divider()


st.sidebar.info(
    """
AI Code Review Agent

Features:

✓ Syntax Validation

✓ Code Quality Analysis

✓ Security Vulnerability Detection

✓ OWASP Based Review

✓ RAG Knowledge Base
"""
)



# =====================================================
# NEW REVIEW
# =====================================================

if page == "🏠 New Review":

    st.title(
        "AI Code Review & Security Analysis Agent"
    )


    st.write(
        """
Upload a **Python** or **Java** source file,
or paste your code directly.

The system performs:

- Language Detection
- Syntax Validation
- Code Quality Analysis
- Security Vulnerability Scanning
- Consolidated Review Report
"""
    )


    st.divider()


    left_column, right_column = st.columns(
        [2.3, 1]
    )



    # =================================================
    # Source Code Panel
    # =================================================

    with left_column:

        st.subheader(
            "Source Code"
        )


        uploaded_file = st.file_uploader(
            "Upload Python or Java File",
            type=[
                "py",
                "java"
            ]
        )


        st.markdown(
            "### OR"
        )


        code = st.text_area(
            "Paste your code",
            height=380,
            placeholder=
            "Paste Python or Java code here..."
        )



    # =================================================
    # Options Panel
    # =================================================

    with right_column:

        st.subheader(
            "Options"
        )


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


        st.divider()


        st.info(
            """
### Analysis Includes

✅ Language Detection

✅ Syntax Validation

✅ Code Analysis Agent

✅ Security Agent

✅ Severity Classification

✅ Recommendations
"""
        )
    # =====================================================
    # Analyze Button
    # =====================================================

    if analyze:

        if uploaded_file is None and code.strip() == "":

            st.error(
                "Please upload a file or paste source code."
            )


        else:

            # ---------------------------------------------
            # Read Source Code
            # ---------------------------------------------

            if uploaded_file is not None:

                source_code = uploaded_file.read().decode(
                    "utf-8"
                )

                file_name = uploaded_file.name


            else:

                source_code = code

                file_name = "Pasted Code"


            # ---------------------------------------------
            # Language Detection
            # ---------------------------------------------

            if language == "Auto Detect":

                language = detect_language(
                    source_code,
                    file_name
                )

            # ---------------------------------------------
            # Syntax Validation
            # ---------------------------------------------

            valid, message = validate_code(
                source_code,
                language
            )


            st.divider()


            st.subheader(
                "Submission Details"
            )


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Language",
                language
            )


            col2.metric(
                "Lines",
                len(
                    source_code.splitlines()
                )
            )


            col3.metric(
                "File",
                file_name
            )



            # =====================================================
            # If Syntax Valid
            # =====================================================

            if valid:

                st.success(
                    message
                )


                # ---------------------------------------------
                # Run Agents
                # ---------------------------------------------

                result = orchestrator.analyze_code(
                    source_code,
                    language
                )


                summary = result.get(
                    "summary",
                    {}
                )


                findings = result.get(
                    "findings",
                    []
                )



                st.divider()


                # =====================================================
                # Analysis Summary
                # =====================================================

                st.subheader(
                    "Analysis Summary"
                )


                col1, col2, col3, col4, col5 = st.columns(5)


                col1.metric(
                    "Critical",
                    summary.get(
                        "CRITICAL",
                        0
                    )
                )


                col2.metric(
                    "High",
                    summary.get(
                        "HIGH",
                        0
                    )
                )


                col3.metric(
                    "Medium",
                    summary.get(
                        "MEDIUM",
                        0
                    )
                )


                col4.metric(
                    "Low",
                    summary.get(
                        "LOW",
                        0
                    )
                )


                col5.metric(
                    "Total",
                    len(findings)
                )



                st.divider()


                # =====================================================
                # Findings
                # =====================================================

                st.subheader(
                    "Findings"
                )


                if len(findings) == 0:

                    st.success(
                        "No code quality or security issues detected."
                    )


                else:

                    for index, finding in enumerate(
                        findings,
                        start=1
                    ):


                        severity = finding.get(
                            "severity",
                            "LOW"
                        )


                        issue_type = finding.get(
                            "type",
                            "Issue"
                        )


                        title = (
                            f"Finding {index} • "
                            f"{severity} • "
                            f"{issue_type}"
                        )


                        with st.expander(title):


                            left, right = st.columns(2)



                            with left:

                                st.write(
                                    "**Agent**"
                                )

                                st.write(
                                    finding.get(
                                        "agent",
                                        "Unknown"
                                    )
                                )


                                st.write(
                                    "**Severity**"
                                )

                                st.write(
                                    finding.get(
                                        "severity",
                                        "LOW"
                                    )
                                )


                                st.write(
                                    "**Line Number**"
                                )

                                st.write(
                                    finding.get(
                                        "line",
                                        "N/A"
                                    )
                                )



                            with right:

                                st.write(
                                    "**Issue Type**"
                                )

                                st.write(
                                    finding.get(
                                        "type",
                                        "Unknown"
                                    )
                                )



                            st.write(
                                "**Description**"
                            )


                            st.write(
                                finding.get(
                                    "description",
                                    "No description available."
                                )
                            )



                            st.write(
                                "**Recommendation**"
                            )


                            st.success(
                                finding.get(
                                    "recommendation",
                                    "No recommendation available."
                                )
                            )



            # =====================================================
            # Syntax Invalid
            # =====================================================

            else:

                st.error(
                    message
                )

# =====================================================
# KNOWLEDGE BASE
# =====================================================

elif page == "📚 Knowledge Base":

    st.title(
        "Secure Coding Knowledge Base"
    )


    st.write(
        """
The knowledge base stores secure coding guidelines,
OWASP documentation, and security references
used by the RAG pipeline.
"""
    )


    st.divider()


    st.subheader(
        "Indexed Documents"
    )


    documents = [

        "OWASP Top 10 2025",

        "OWASP Top 10",

        "Broken Access Control",

        "Cryptographic Failures",

        "Insecure Design",

        "Security Misconfiguration",

        "Vulnerable Components",

        "Weak Authentication",

        "SQL Injection",

        "SSRF Protection",

        "XML Security",

        "SSL Security",

        "Java Secure Coding",

        "Python Secure Coding",

        "Python Secrets Module",

        "Pickle Security",

        "Subprocess Security",

        "Logging & Monitoring",

        "Secure Coding Guide"
    ]


    for doc in documents:

        st.write(
            f"• {doc}"
        )



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


                st.success(
                    result
                )


            except Exception as e:

                st.error(
                    f"Knowledge Base Error:\n\n{e}"
                )





# =====================================================
# REPORTS
# =====================================================

elif page == "📄 Reports":

    st.title(
        "Reports"
    )


    st.write(
        """
All generated code review reports will appear here.
"""
    )


    st.divider()


    st.info(
        "No reports generated yet."
    )





# =====================================================
# HISTORY
# =====================================================

elif page == "🕘 History":

    st.title(
        "Analysis History"
    )


    st.write(
        """
Previously analyzed files and security reports
will appear here.
"""
    )


    st.divider()


    st.info(
        "History is currently empty."
    )
# =====================================================
# SETTINGS
# =====================================================

elif page == "⚙ Settings":

    st.title(
        "Settings"
    )


    st.divider()



    theme = st.selectbox(
        "Application Theme",
        [
            "Dark",
            "Light"
        ]
    )



    default_language = st.selectbox(
        "Default Language",
        [
            "Auto Detect",
            "Python",
            "Java"
        ]
    )



    notifications = st.checkbox(
        "Enable Notifications"
    )



    auto_detect = st.checkbox(
        "Automatically Detect Language",
        value=True
    )



    st.divider()



    if st.button(
        "Save Settings",
        use_container_width=True
    ):

        st.success(
            "Settings saved successfully."
        )





# =====================================================
# FOOTER
# =====================================================

st.divider()


left, center, right = st.columns(3)



with left:

    st.caption(
        "AI Code Review & Security Analysis Agent"
    )



with center:

    st.caption(
        "Milestone 2"
    )



with right:

    st.caption(
        "Python • Java • Streamlit"
    )