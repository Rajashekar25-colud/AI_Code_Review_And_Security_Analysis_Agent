import streamlit as st


# ==========================================================
# Section Header
# ==========================================================

def section_header(title, icon=""):

    st.markdown(f"## {icon} {title}")
    st.divider()


# ==========================================================
# Status Card
# ==========================================================

def status_card(title, value, color="blue"):

    colors = {
        "blue": "#1976d2",
        "green": "#2e7d32",
        "orange": "#ef6c00",
        "red": "#c62828",
        "purple": "#6a1b9a"
    }

    st.markdown(
        f"""
        <div style="
        background-color:{colors.get(color,'#1976d2')};
        padding:18px;
        border-radius:10px;
        color:white;
        text-align:center;
        ">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# Severity Badge
# ==========================================================

def severity_badge(severity):

    severity = str(severity).upper()

    color = {
        "CRITICAL": "#d32f2f",
        "HIGH": "#ef6c00",
        "MEDIUM": "#f9a825",
        "LOW": "#2e7d32"
    }.get(severity, "#546e7a")

    st.markdown(
        f"""
        <span style="
        background:{color};
        color:white;
        padding:5px 10px;
        border-radius:6px;
        font-size:14px;
        font-weight:bold;">
        {severity}
        </span>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# Finding Card
# ==========================================================

def finding_card(finding, index):

    severity = finding.get("severity", "LOW")

    title = finding.get("type", "Issue")

    with st.expander(f"Finding {index} • {title}"):

        c1, c2 = st.columns(2)

        with c1:

            st.write("**Agent**")
            st.write(finding.get("agent", "-"))

            st.write("**Severity**")
            severity_badge(severity)

            st.write("**Line**")
            st.write(finding.get("line", "-"))

        with c2:

            st.write("**Issue Type**")
            st.write(finding.get("type", "-"))

            st.write("**Category**")
            st.write(finding.get("category", "-"))

        st.markdown("### Description")

        st.write(
            finding.get(
                "description",
                "No description available."
            )
        )

        st.markdown("### Recommendation")

        st.success(
            finding.get(
                "recommendation",
                "No recommendation available."
            )
        )


# ==========================================================
# Empty State
# ==========================================================

def empty_state(message):

    st.info(message)


# ==========================================================
# Success Banner
# ==========================================================

def success_banner(message):

    st.success(message)


# ==========================================================
# Error Banner
# ==========================================================

def error_banner(message):

    st.error(message)


# ==========================================================
# Loading Spinner
# ==========================================================

def loading(message="Processing..."):

    return st.spinner(message)


# ==========================================================
# Metric Row
# ==========================================================

def metric_row(metrics):

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        col.metric(

            metric.get("label", ""),

            metric.get("value", ""),

            metric.get("delta", None)

        )


# ==========================================================
# File Information Card
# ==========================================================

def file_info(file_name, language, lines):

    c1, c2, c3 = st.columns(3)

    c1.metric("Language", language)

    c2.metric("Lines", lines)

    c3.metric("File", file_name)


# ==========================================================
# Code Health Progress
# ==========================================================

def health_progress(score):

    st.progress(score / 100)

    st.write(f"Overall Code Health Score: **{score}/100**")


# ==========================================================
# Page Footer
# ==========================================================

def footer():

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.caption("AI Code Review Agent")

    c2.caption("LangGraph • Streamlit • Groq")

    c3.caption("Python • Java • OWASP")