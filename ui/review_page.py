import streamlit as st

from modules.language_detector import detect_language
from modules.syntax_validator import validate_code
from modules.report_generator import generate_pdf
from database.repository import save_review


def render_review_page(orchestrator):

    user = st.session_state.get("user")
    display_name = user.get("name") if user else None

    if display_name:
        st.title(f"👋 Hello, {display_name}")
        st.caption(
            "Paste or upload Python or Java source code and I'll "
            "review it for quality issues and security vulnerabilities."
        )
    else:
        st.title("🤖 Smart Code Inspection Platform")
        st.markdown(
            "Analyze **Python** or **Java** source code for vulnerabilities "
            "using a multi-agent AI pipeline."
        )

    st.markdown(
        """
**Features**

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

    # ------------------------------------------------------
    # Run analysis only when the button was just clicked.
    # The RESULT itself is stored in session state so it (and
    # the dashboard/chat below) keep showing on every later
    # rerun - e.g. when the person types in the chat box,
    # which triggers a full script rerun in Streamlit.
    #
    # On any failure path (no input, syntax error), the stored
    # result is explicitly cleared - otherwise a stale dashboard
    # from a PREVIOUS successful review would keep rendering
    # underneath the new error message, which is misleading.
    # ------------------------------------------------------

    if analyze:

        if uploaded_file is None and not code.strip():

            st.error("Please upload a file or paste source code.")
            st.session_state.review_result = None

        else:

            if uploaded_file:

                source_code = uploaded_file.read().decode("utf-8")
                filename = uploaded_file.name

            else:

                source_code = code
                filename = "Pasted Code"

            resolved_language = language

            if resolved_language == "Auto Detect":

                resolved_language = detect_language(
                    source_code,
                    filename
                )

            valid, message = validate_code(
                source_code,
                resolved_language
            )

            if not valid:

                st.error(message)
                st.session_state.review_result = None

            else:

                with st.spinner("Analyzing source code..."):

                    if orchestrator is None:

                        from agents.orchestrator import Orchestrator

                        orchestrator = Orchestrator()

                        st.session_state.orchestrator = orchestrator

                    result = orchestrator.analyze_code(
                        source_code,
                        resolved_language
                    )

                result["filename"] = filename
                result["language"] = resolved_language
                result["lines"] = len(source_code.splitlines())

                st.session_state.review_result = result

                # ------------------------------------------
                # Persist to database so it shows up in
                # History and the sidebar's Recent Reviews.
                # ------------------------------------------

                if user:

                    review_id = save_review(
                        user_id=user["id"],
                        filename=filename,
                        language=resolved_language,
                        findings=result.get("findings", []),
                        summary=result.get("pr_summary", "")
                    )

                    st.session_state.active_review_id = review_id

                # Starting a brand new review clears the old
                # chat thread so follow-ups apply to this one.
                thread_key = f"{filename}:{len(result.get('findings', []))}"

                if "chat_threads" not in st.session_state:
                    st.session_state.chat_threads = {}

                st.session_state.chat_threads[thread_key] = []

    # ------------------------------------------------------
    # Always render the current result (if any) - independent
    # of whether Analyze was clicked on THIS run.
    # ------------------------------------------------------

    result = st.session_state.get("review_result")

    if not result:
        return

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Language", result.get("language", "Unknown"))
    c2.metric("Lines", result.get("lines", 0))
    c3.metric("File", result.get("filename", "Unknown"))

    st.divider()

    # Import dashboard lazily to avoid requiring pandas at app startup
    from ui.dashboard import render_dashboard

    render_dashboard(result)

    findings = result.get("findings", [])

    counts = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for finding in findings:

        severity = str(finding.get("severity", "LOW")).upper()

        if severity == "CRITICAL":
            counts["Critical"] += 1

        elif severity == "HIGH":
            counts["High"] += 1

        elif severity == "MEDIUM":
            counts["Medium"] += 1

        else:
            counts["Low"] += 1

    pdf = generate_pdf(
        language=result.get("language", "Unknown"),
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

    # ------------------------------------------------------
    # Embedded follow-up chat, right under the results -
    # no separate "AI Assistant" nav page. This now survives
    # every rerun since it's outside the "if analyze" block.
    # ------------------------------------------------------

    st.divider()

    from ui.assistant import render_assistant_page

    render_assistant_page(result)