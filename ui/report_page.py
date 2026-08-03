import os
import streamlit as st

from modules.report_generator import generate_pdf


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

    pdf_path = generate_pdf(

        language=language,

        findings=findings,

        summary=counts

    )

    st.subheader("📥 Download Report")

    if os.path.exists(pdf_path):

        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            st.download_button(

                label="📄 Download PDF Report",

                data=pdf_file,

                file_name="AI_Code_Review_Report.pdf",

                mime="application/pdf",

                width="stretch"

            )

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