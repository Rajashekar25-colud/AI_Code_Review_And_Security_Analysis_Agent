import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import json
import os

from modules.score_calculator import calculate_score


# ==========================================================
# Severity Colors
# ==========================================================

SEVERITY_COLORS = {
    "CRITICAL": "#d32f2f",
    "HIGH": "#f57c00",
    "MEDIUM": "#fbc02d",
    "LOW": "#43a047"
}


# ==========================================================
# Radar Dimensions
# ==========================================================

RADAR_DIMENSIONS = [
    "Security",
    "Quality",
    "Maintainability",
    "Reliability",
    "Complexity"
]


# ==========================================================
# Risk Thresholds (config-driven, not hardcoded)
# ==========================================================

_risk_thresholds = None


def _load_risk_thresholds():

    global _risk_thresholds

    if _risk_thresholds is None:

        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config",
            "risk_thresholds.json"
        )

        with open(path, "r", encoding="utf-8") as f:
            _risk_thresholds = json.load(f)

    return _risk_thresholds


def _get_risk_band(score):

    for band in _load_risk_thresholds():

        if score >= band["min_score"]:
            return band

    return _load_risk_thresholds()[-1]


def get_risk_level(score):
    return _get_risk_band(score)["label"]


# ==========================================================
# Safely Count Findings
# ==========================================================

def get_severity_counts(findings):

    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for finding in findings:

        severity = str(finding.get("severity", "LOW")).upper()

        if severity not in counts:
            severity = "LOW"

        counts[severity] += 1

    return counts


# ==========================================================
# Calculate Overall Code Health
# ==========================================================

def calculate_health_score(findings):
    return calculate_score(findings)


# ==========================================================
# Radar Scores
# ==========================================================

def calculate_radar_scores(findings):

    security_findings = [
        f for f in findings
        if f.get("agent") == "Security Vulnerability Agent"
    ]

    complexity_findings = [
        f for f in findings
        if f.get("tool") == "Radon"
    ]

    quality_findings = [
        f for f in findings
        if f.get("agent") == "Code Analysis Agent"
        and f.get("tool") != "Radon"
    ]

    reliability_findings = [
        f for f in findings
        if f.get("tool") == "SpotBugs"
    ]

    if not reliability_findings:
        reliability_findings = findings

    return {
        "Security": calculate_score(security_findings),
        "Quality": calculate_score(quality_findings),
        "Maintainability": calculate_score(quality_findings + complexity_findings),
        "Reliability": calculate_score(reliability_findings),
        "Complexity": calculate_score(complexity_findings)
    }


# ==========================================================
# OWASP Coverage (data helper kept - used by Reports page;
# the dashboard widget itself was removed per request)
# ==========================================================

def get_owasp_categories(findings):

    categories = set()

    for finding in findings:

        category = finding.get("owasp_category")

        if category:
            categories.add(category)

    return sorted(categories)


# ==========================================================
# Findings DataFrame
# ==========================================================

def findings_dataframe(findings):

    rows = []

    for finding in findings:

        rows.append({
            "Agent": finding.get("agent", ""),
            "Severity": finding.get("severity", ""),
            "Type": finding.get("type", ""),
            "Line": finding.get("line", ""),
            "Description": finding.get("description", ""),
            "Recommendation": finding.get("recommendation", "")
        })

    if not rows:

        return pd.DataFrame(
            columns=[
                "Agent", "Severity", "Type",
                "Line", "Description", "Recommendation"
            ]
        )

    return pd.DataFrame(rows)


# ==========================================================
# Dashboard Metric Cards
# ==========================================================

def render_metrics(findings):

    counts = get_severity_counts(findings)
    score = calculate_health_score(findings)
    risk = get_risk_level(score)
    total = len(findings)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("Critical", counts["CRITICAL"])
    c2.metric("High", counts["HIGH"])
    c3.metric("Medium", counts["MEDIUM"])
    c4.metric("Low", counts["LOW"])
    c5.metric("Total Issues", total)
    c6.metric("Health Score", f"{score}/100")

    st.success(f"Overall Code Health : **{risk}**")


# ==========================================================
# Prepare Dashboard Data
# ==========================================================

def prepare_dashboard_data(result):

    findings = result.get("findings", [])
    remediation = result.get("remediation", {})
    summary = result.get("pr_summary", "")

    score = calculate_health_score(findings)

    return {
        "findings": findings,
        "remediation": remediation,
        "summary": summary,
        "counts": get_severity_counts(findings),
        "score": score,
        "risk": get_risk_level(score),
        "owasp_categories": get_owasp_categories(findings),
        "table": findings_dataframe(findings)
    }


# ==========================================================
# Severity Bar Chart
# ==========================================================

def render_severity_bar(findings):

    counts = get_severity_counts(findings)

    df = pd.DataFrame({
        "Severity": list(counts.keys()),
        "Issues": list(counts.values())
    })

    fig = px.bar(
        df,
        x="Severity",
        y="Issues",
        color="Severity",
        color_discrete_map=SEVERITY_COLORS,
        text="Issues"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        title="Severity Comparison",
        height=420,
        showlegend=False
    )

    st.plotly_chart(fig, width="stretch")


# ==========================================================
# Radar Chart
# ==========================================================

def render_radar_chart(findings):

    radar_scores = calculate_radar_scores(findings)

    categories = RADAR_DIMENSIONS + [RADAR_DIMENSIONS[0]]

    values = (
        [radar_scores.get(dim, 100) for dim in RADAR_DIMENSIONS]
        + [radar_scores.get(RADAR_DIMENSIONS[0], 100)]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Score",
            line=dict(color="#5b8def"),
            fillcolor="rgba(91, 141, 239, 0.35)"
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Score Radar",
        height=420,
        margin=dict(t=60, b=10, l=40, r=40)
    )

    st.plotly_chart(fig, width="stretch")


# ==========================================================
# Code Health Gauge
# ==========================================================

def render_health_gauge(findings):

    score = calculate_health_score(findings)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Overall Code Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "royalblue"},
                "steps": [
                    {"range": [0, 40], "color": "#d32f2f"},
                    {"range": [40, 60], "color": "#f57c00"},
                    {"range": [60, 80], "color": "#fbc02d"},
                    {"range": [80, 100], "color": "#43a047"}
                ]
            }
        )
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, width="stretch")


# ==========================================================
# Complete Dashboard (Executive View)
#
# OWASP Coverage widget removed from this view per request -
# get_owasp_categories() is still used by the Reports page.
# ==========================================================

def render_dashboard(result):

    dashboard = prepare_dashboard_data(result)
    findings = dashboard["findings"]

    render_metrics(findings)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        render_severity_bar(findings)

    with col2:
        render_health_gauge(findings)

    st.divider()

    render_radar_chart(findings)

    if dashboard["remediation"]:

        st.divider()
        st.subheader("🛠 Remediation Suggestions")

        remediation = dashboard["remediation"]

        if isinstance(remediation, dict) and remediation.get("error"):

            st.error(
                "⚠️ AI remediation could not be generated right now "
                "(a connection issue occurred with the AI model). "
                "The security findings above are still accurate - "
                "only the AI-written suggestions failed. Try running "
                "the review again."
            )

        else:

            if isinstance(remediation, dict):
                recommendations = remediation.get("recommendations", remediation)
            else:
                recommendations = remediation

            if isinstance(recommendations, list):

                for index, recommendation in enumerate(recommendations, start=1):

                    st.markdown(f"### Recommendation {index}")

                    if isinstance(recommendation, dict):

                        for key, value in recommendation.items():
                            st.markdown(f"**{key.replace('_', ' ').title()}**")
                            st.write(value)

                    else:
                        st.write(recommendation)

                    st.divider()

            elif isinstance(recommendations, str):
                st.markdown(recommendations)

            else:
                st.info("No remediation content available for this review.")

    if dashboard["summary"]:

        st.divider()
        st.subheader("📋 Pull Request Summary")

        summary = dashboard["summary"]

        if isinstance(summary, str) and "failed" in summary.lower():

            st.warning(
                "⚠️ The AI-generated PR summary could not be created "
                "right now due to a connection issue. The findings "
                "and severity breakdown above are still accurate. "
                "Try running the review again."
            )

        else:
            st.markdown(summary)