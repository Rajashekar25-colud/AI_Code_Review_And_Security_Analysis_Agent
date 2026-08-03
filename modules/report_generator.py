import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


# ==================================================
# PDF Styles
# ==================================================

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading = styles["Heading2"]

normal = styles["BodyText"]


# ==================================================
# PDF Generator
# ==================================================

def generate_pdf(
    language,
    findings,
    summary
):

    # ----------------------------------------------
    # Create report directory dynamically
    # ----------------------------------------------

    report_directory = os.path.join(
        os.getcwd(),
        "generated_reports"
    )

    os.makedirs(
        report_directory,
        exist_ok=True
    )


    pdf_path = os.path.join(
        report_directory,
        "AI_Code_Review_Report.pdf"
    )


    doc = SimpleDocTemplate(
        pdf_path
    )


    story = []


    # ==============================================
    # Title
    # ==============================================

    story.append(
        Paragraph(
            "AI Code Review & Security Analysis Report",
            title_style
        )
    )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )


    story.append(
        Paragraph(
            f"<b>Language:</b> {language}",
            normal
        )
    )


    story.append(
        Spacer(
            1,
            0.2 * inch
        )
    )


    # ==============================================
    # Analysis Summary
    # ==============================================

    story.append(
        Paragraph(
            "Analysis Summary",
            heading
        )
    )


    summary_table = Table(
        [
            [
                "Severity",
                "Count"
            ],
            [
                "Critical",
                summary.get(
                    "Critical",
                    0
                )
            ],
            [
                "High",
                summary.get(
                    "High",
                    0
                )
            ],
            [
                "Medium",
                summary.get(
                    "Medium",
                    0
                )
            ],
            [
                "Low",
                summary.get(
                    "Low",
                    0
                )
            ],
            [
                "Total",
                summary.get(
                    "Total",
                    0
                )
            ]
        ],

        colWidths=[
            150,
            80
        ]
    )


    summary_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    1,
                    colors.black
                ),

                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.lightgrey
                ),

                (
                    "ALIGN",
                    (1,1),
                    (1,-1),
                    "CENTER"
                ),

                (
                    "FONTNAME",
                    (0,0),
                    (-1,0),
                    "Helvetica-Bold"
                )
            ]
        )
    )


    story.append(
        summary_table
    )


    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )


    # ==============================================
    # Findings
    # ==============================================

    story.append(
        Paragraph(
            "Detailed Findings",
            heading
        )
    )


    if not findings:


        story.append(
            Paragraph(
                "No issues detected.",
                normal
            )
        )


    else:


        for index, finding in enumerate(
            findings,
            start=1
        ):


            story.append(
                Paragraph(
                    f"Finding {index}",
                    styles["Heading3"]
                )
            )


            details = [

                (
                    "Agent",
                    finding.get(
                        "agent",
                        "Unknown"
                    )
                ),

                (
                    "Severity",
                    finding.get(
                        "severity",
                        "LOW"
                    )
                ),

                (
                    "Issue",
                    finding.get(
                        "type",
                        "Unknown"
                    )
                ),

                (
                    "Line",
                    finding.get(
                        "line",
                        "N/A"
                    )
                ),

                (
                    "Description",
                    finding.get(
                        "description",
                        "No description available"
                    )
                ),

                (
                    "Recommendation",
                    finding.get(
                        "recommendation",
                        "No recommendation available"
                    )
                )
            ]


            for key, value in details:


                story.append(
                    Paragraph(
                        f"<b>{key}:</b> {value}",
                        normal
                    )
                )


            story.append(
                Spacer(
                    1,
                    0.25 * inch
                )
            )


    # ==============================================
    # Generate PDF
    # ==============================================

    doc.build(
        story
    )


    return pdf_path