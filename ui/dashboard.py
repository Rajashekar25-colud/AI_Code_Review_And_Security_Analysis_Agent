import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

        severity = str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper()

        if severity not in counts:
            severity = "LOW"

        counts[severity] += 1

    return counts


# ==========================================================
# Calculate Overall Code Health
# ==========================================================

def calculate_health_score(findings):

    score = 100

    weights = {
        "CRITICAL": 25,
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 3
    }

    for finding in findings:

        severity = str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper()

        score -= weights.get(
            severity,
            3
        )

    return max(score, 0)


# ==========================================================
# Risk Level
# ==========================================================

def get_risk_level(score):

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 60:
        return "Moderate"

    if score >= 40:
        return "Poor"

    return "Critical"


# ==========================================================
# Agent Contribution
# ==========================================================

def get_agent_statistics(findings):

    stats = {}

    for finding in findings:

        agent = finding.get(
            "agent",
            "Unknown Agent"
        )

        stats[agent] = stats.get(
            agent,
            0
        ) + 1

    return stats


# ==========================================================
# Findings DataFrame
# ==========================================================

def findings_dataframe(findings):

    rows = []

    for finding in findings:

        rows.append({

            "Agent": finding.get(
                "agent",
                ""
            ),

            "Severity": finding.get(
                "severity",
                ""
            ),

            "Type": finding.get(
                "type",
                ""
            ),

            "Line": finding.get(
                "line",
                ""
            ),

            "Description": finding.get(
                "description",
                ""
            ),

            "Recommendation": finding.get(
                "recommendation",
                ""
            )

        })

    if not rows:

        return pd.DataFrame(
            columns=[
                "Agent",
                "Severity",
                "Type",
                "Line",
                "Description",
                "Recommendation"
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

    st.success(
        f"Overall Code Health : **{risk}**"
    )


# ==========================================================
# Prepare Dashboard Data
# ==========================================================

def prepare_dashboard_data(result):

    findings = result.get(
        "findings",
        []
    )

    remediation = result.get(
        "remediation",
        {}
    )

    summary = result.get(
        "pr_summary",
        ""
    )

    score = calculate_health_score(findings)

    return {

        "findings": findings,

        "remediation": remediation,

        "summary": summary,

        "counts": get_severity_counts(findings),

        "score": score,

        "risk": get_risk_level(score),

        "agent_stats": get_agent_statistics(findings),

        "table": findings_dataframe(findings)

    }
    # ==========================================================
# Severity Distribution Pie Chart
# ==========================================================

def render_severity_pie(findings):

    counts = get_severity_counts(findings)

    df = pd.DataFrame(
        {
            "Severity": list(counts.keys()),
            "Count": list(counts.values())
        }
    )

    fig = px.pie(
        df,
        names="Severity",
        values="Count",
        color="Severity",
        color_discrete_map=SEVERITY_COLORS,
        hole=0.45
    )

    fig.update_layout(
        title="Severity Distribution",
        height=420,
        legend_title="Severity"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==========================================================
# Severity Bar Chart
# ==========================================================

def render_severity_bar(findings):

    counts = get_severity_counts(findings)

    df = pd.DataFrame(
        {
            "Severity": list(counts.keys()),
            "Issues": list(counts.values())
        }
    )

    fig = px.bar(
        df,
        x="Severity",
        y="Issues",
        color="Severity",
        color_discrete_map=SEVERITY_COLORS,
        text="Issues"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        title="Severity Comparison",
        height=420,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==========================================================
# Agent Contribution Chart
# ==========================================================

def render_agent_statistics(findings):

    stats = get_agent_statistics(findings)

    if not stats:

        st.info(
            "No agent statistics available."
        )

        return

    df = pd.DataFrame(
        {
            "Agent": list(stats.keys()),
            "Findings": list(stats.values())
        }
    )

    fig = px.bar(
        df,
        x="Agent",
        y="Findings",
        text="Findings",
        color="Findings"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        title="Agent Contribution",
        height=420
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==========================================================
# Findings Timeline
# ==========================================================

def render_timeline(findings):

    if not findings:

        st.info(
            "No findings available."
        )

        return

    data = []

    for index, finding in enumerate(
        findings,
        start=1
    ):

        data.append(
            {
                "Finding": index,
                "Severity": finding.get(
                    "severity",
                    "LOW"
                )
            }
        )

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Finding",
        y=[1] * len(df),
        color="Severity",
        markers=True,
        color_discrete_map=SEVERITY_COLORS
    )

    fig.update_layout(
        title="Finding Timeline",
        showlegend=True,
        yaxis_visible=False,
        xaxis_title="Finding Number",
        height=350
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==========================================================
# Findings Table
# ==========================================================

def render_findings_table(findings):

    st.subheader(
        "Detailed Findings"
    )

    df = findings_dataframe(findings)

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


# ==========================================================
# Code Health Gauge
# ==========================================================

def render_health_gauge(findings):

    score = calculate_health_score(findings)

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={
                "text": "Overall Code Health Score"
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "bar": {
                    "color": "royalblue"
                },

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "#d32f2f"
                    },

                    {
                        "range": [40, 60],
                        "color": "#f57c00"
                    },

                    {
                        "range": [60, 80],
                        "color": "#fbc02d"
                    },

                    {
                        "range": [80, 100],
                        "color": "#43a047"
                    }

                ]
            }

        )

    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )
    # ==========================================================
# Download Findings CSV
# ==========================================================

def download_findings(findings):

    df = findings_dataframe(findings)

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="⬇ Download Findings CSV",

        data=csv,

        file_name="findings.csv",

        mime="text/csv",

        width="stretch"

    )


# ==========================================================
# Complete Dashboard
# ==========================================================

def render_dashboard(result):

    dashboard = prepare_dashboard_data(result)

    findings = dashboard["findings"]

    render_metrics(findings)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        render_severity_pie(findings)

    with col2:

        render_health_gauge(findings)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        render_severity_bar(findings)

    with col2:

        render_agent_statistics(findings)

    st.divider()

    render_timeline(findings)

    st.divider()

    render_findings_table(findings)

    st.divider()

    download_findings(findings)

    if dashboard["remediation"]:

        st.divider()

        st.subheader("🛠 Remediation Suggestions")

        remediation = dashboard["remediation"]

        if isinstance(remediation, dict):

            recommendations = remediation.get(
                "recommendations",
                remediation
            )

        else:

            recommendations = remediation

        if isinstance(recommendations, list):

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

            st.markdown(recommendations)

    if dashboard["summary"]:

        st.divider()

        st.subheader("📋 Pull Request Summary")

        st.markdown(
            dashboard["summary"]
        )