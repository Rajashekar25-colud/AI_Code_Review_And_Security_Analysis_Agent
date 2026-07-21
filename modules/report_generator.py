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

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading = styles["Heading2"]
normal = styles["BodyText"]


def generate_pdf(language, findings, summary):

    filename = "AI_Code_Review_Report.pdf"

    doc = SimpleDocTemplate(filename)

    story = []

    # ==========================================
    # Title
    # ==========================================

    story.append(
        Paragraph(
            "AI Code Review & Security Analysis Report",
            title_style,
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            f"<b>Language:</b> {language}",
            normal,
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    # ==========================================
    # Summary
    # ==========================================

    story.append(
        Paragraph(
            "Analysis Summary",
            heading,
        )
    )

    summary_table = Table(
        [
            ["Severity", "Count"],
            ["Critical", summary.get("Critical", 0)],
            ["High", summary.get("High", 0)],
            ["Medium", summary.get("Medium", 0)],
            ["Low", summary.get("Low", 0)],
            ["Total", summary.get("Total", 0)],
        ],
        colWidths=[150, 80],
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    story.append(summary_table)

    story.append(Spacer(1, 0.3 * inch))

    # ==========================================
    # Findings
    # ==========================================

    story.append(
        Paragraph(
            "Detailed Findings",
            heading,
        )
    )

    if len(findings) == 0:

        story.append(
            Paragraph(
                "No issues detected.",
                normal,
            )
        )

    else:

        for i, finding in enumerate(findings, start=1):

            story.append(
                Paragraph(
                    f"<b>Finding {i}</b>",
                    styles["Heading3"],
                )
            )

            story.append(
                Paragraph(
                    f"<b>Agent:</b> {finding.get('agent','Unknown')}",
                    normal,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Severity:</b> {finding.get('severity','LOW')}",
                    normal,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Issue:</b> {finding.get('type','Unknown')}",
                    normal,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Line:</b> {finding.get('line','N/A')}",
                    normal,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Description:</b> {finding.get('description','No description available.')}",
                    normal,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Recommendation:</b> {finding.get('recommendation','No recommendation available.')}",
                    normal,
                )
            )

            story.append(Spacer(1, 0.25 * inch))

    # ==========================================
    # Build PDF
    # ==========================================

    doc.build(story)

    return filename