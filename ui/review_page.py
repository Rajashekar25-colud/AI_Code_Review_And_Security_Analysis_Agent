import streamlit as st

from modules.language_detector import detect_language
from modules.syntax_validator import validate_code
from modules.report_generator import generate_pdf


def render_review_page(orchestrator):

    st.title("🤖 AI Code Review & Security Analysis Agent")

    st.markdown(
        """
Analyze **Python** or **Java** source code using a multi-agent AI pipeline.

### Features

- 🔍 Automatic Language Detection
- ✅ Syntax Validation
- 💡 Code Quality Analysis
- 🛡️ Security Vulnerability Detection
- 🔧 AI Remediation Suggestions
- 📝 Pull Request Summary
- 📊 Interactive Dashboard
- 📄 PDF Report
"""
    )

    st.divider()

    left, right = st.columns([3, 1])

    with left:

        uploaded_file = st.file_uploader(
            "Upload Python or Java File",
            type=["py", "java"]
        )

        st.markdown("### OR")

        code = st.text_area(
            "Paste Source Code",
            height=450,
            placeholder="Paste your source code here..."
        )

    with right:

        language = st.selectbox(
            "Language",
            [
                "Auto Detect",
                "Python",
                "Java"
            ]
        )

        analyze = st.button(
            "🚀 Analyze Code",
            width="stretch"
        )

    if not analyze:
        return

    if uploaded_file is None and not code.strip():

        st.error("Please upload a file or paste source code.")
        return

    if uploaded_file:

        source_code = uploaded_file.read().decode("utf-8")
        filename = uploaded_file.name

    else:

        source_code = code
        filename = "Pasted Code"

    if language == "Auto Detect":

        language = detect_language(
            source_code,
            filename
        )

    valid, message = validate_code(
        source_code,
        language
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Language",
        language
    )

    c2.metric(
        "Lines",
        len(source_code.splitlines())
    )

    c3.metric(
        "File",
        filename
    )

    if not valid:

        st.error(message)
        return

    st.success(message)

    with st.spinner("Analyzing source code..."):

        # Lazily instantiate the orchestrator if it was not created at startup.
        if orchestrator is None:

            from agents.orchestrator import Orchestrator

            orchestrator = Orchestrator()

            st.session_state.orchestrator = orchestrator

        result = orchestrator.analyze_code(
            source_code,
            language
        )

    # Save for other pages
    st.session_state.review_result = result

    st.divider()

    # Import dashboard lazily to avoid requiring pandas at app startup
    from ui.dashboard import render_dashboard

    render_dashboard(result)

    findings = result.get(
        "findings",
        []
    )

    counts = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for finding in findings:

        severity = finding.get(
            "severity",
            "LOW"
        ).upper()

        if severity == "CRITICAL":
            counts["Critical"] += 1

        elif severity == "HIGH":
            counts["High"] += 1

        elif severity == "MEDIUM":
            counts["Medium"] += 1

        else:
            counts["Low"] += 1

    pdf = generate_pdf(
        language=language,
        findings=findings,
        summary={
            **counts,
            "Total": len(findings)
        }
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=open(pdf, "rb"),
        file_name="AI_Code_Review_Report.pdf",
        mime="application/pdf",
        width="stretch"
    )