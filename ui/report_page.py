import os
import streamlit as st

from modules.report_generator import generate_pdf
from ui.dashboard import SEVERITY_COLORS


def render_findings_cards(findings):
    """
    Detailed findings, shown as expandable cards instead of a
    raw table. No line numbers are shown - only the information
    a reviewer/customer actually needs to act on the finding.
    """

    st.subheader("Detailed Findings")

    if not findings:
        st.success("No findings were reported for this review.")
        return

    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

    ordered = sorted(
        findings,
        key=lambda f: severity_rank.get(
            str(f.get("severity", "LOW")).upper(), 4
        )
    )

    for index, finding in enumerate(ordered, start=1):

        severity = str(finding.get("severity", "LOW")).upper()
        color = SEVERITY_COLORS.get(severity, "#888")
        title = (
            finding.get("type")
            or finding.get("category")
            or "Finding"
        )
        agent = finding.get("agent", "Unknown Agent")

        with st.expander(f"{severity} · {title}", expanded=False):

            st.markdown(
                f"<span style='color:{color};font-weight:700;'>"
                f"{severity}</span> &nbsp;·&nbsp; Detected by "
                f"**{agent}**",
                unsafe_allow_html=True
            )

            description = finding.get("description", "")
            if description:
                st.markdown("**Description**")
                st.write(description)

            recommendation = finding.get("recommendation", "")
            if recommendation:
                st.markdown("**Recommended Fix**")
                st.write(recommendation)

            owasp_category = finding.get("owasp_category")
            if owasp_category:
                st.caption(f"OWASP Category: {owasp_category}")

            reference = finding.get("reference") or finding.get("owasp")
            if reference:
                st.caption(f"Reference: {reference}")


def render_export_options(findings, language, counts):
    """
    Export-only section. PDF only.
    """

    st.subheader("📥 Export")

    pdf_path = generate_pdf(
        language=language,
        findings=findings,
        summary=counts
    )

    if os.path.exists(pdf_path):

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_file,
                file_name="AI_Code_Review_Report.pdf",
                mime="application/pdf",
                width="stretch"
            )


def render_report_page(review_result):
    """
    Reports page.
    Generates and downloads the AI Code Review PDF report.
    """

    st.title("📄 Reports")

    if review_result is None:

        st.info(
            "No review available.\n\n"
            "Run a code review first."
        )

        return

    findings = review_result.get(
        "findings",
        []
    )

    language = review_result.get(
        "language",
        "Unknown"
    )

    summary = review_result.get(
        "pr_summary",
        ""
    )

    remediation = review_result.get(
        "remediation",
        {}
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

    counts["Total"] = len(findings)

    render_export_options(findings, language, counts)

    st.divider()

    render_findings_cards(findings)

    st.divider()

    st.subheader("📋 Pull Request Summary")

    if summary:

        st.markdown(summary)

    else:

        st.info("No PR summary available.")

    st.divider()

    st.subheader("🛠 Remediation Suggestions")

    recommendations = remediation.get(
        "recommendations",
        []
    )

    if isinstance(recommendations, list):

        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                st.markdown(
                    f"### Recommendation {index}"
                )

                if isinstance(recommendation, dict):

                    for key, value in recommendation.items():

                        st.markdown(
                            f"**{key.replace('_', ' ').title()}**"
                        )

                        st.write(value)

                else:

                    st.write(recommendation)

                st.divider()

        else:

            st.success("No remediation required.")

    else:

        st.markdown(recommendations)