import streamlit as st

from database.repository import get_history, get_review_by_id


def render_compare_page():
    """
    Compare two saved reviews for the logged-in user side by side -
    overall score, severity counts, and which findings appear in
    one scan but not the other.
    """

    st.title("🔀 Compare Scans")

    user = st.session_state.get("user")

    if not user:
        st.info("Please log in to compare reviews.")
        return

    reviews = get_history(user["id"])

    if len(reviews) < 2:
        st.info(
            "You need at least two saved reviews to compare.\n\n"
            "Run another code review first."
        )
        return

    options = {
        f"{r.get('filename') or 'Untitled'} — "
        f"{r.get('created_at', '')} (Score {r.get('overall_score', 0)})": r["id"]
        for r in reviews
    }

    col1, col2 = st.columns(2)

    with col1:
        left_label = st.selectbox("Baseline Scan", list(options.keys()), index=1)

    with col2:
        right_label = st.selectbox("Compare Against", list(options.keys()), index=0)

    left_id = options[left_label]
    right_id = options[right_label]

    if left_id == right_id:
        st.warning("Choose two different reviews to compare.")
        return

    left = get_review_by_id(left_id)
    right = get_review_by_id(right_id)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Baseline Score", left.get("overall_score", 0))

    with col2:
        delta = right.get("overall_score", 0) - left.get("overall_score", 0)
        st.metric(
            "Compared Score",
            right.get("overall_score", 0),
            delta=delta
        )

    with col3:
        left_count = len(left.get("findings", []))
        right_count = len(right.get("findings", []))
        st.metric(
            "Findings Count",
            right_count,
            delta=right_count - left_count,
            delta_color="inverse"
        )

    st.divider()

    st.subheader("Severity Breakdown")

    def severity_counts(findings):

        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}

        for finding in findings:

            severity = str(finding.get("severity", "LOW")).upper()

            if severity not in counts:
                severity = "LOW"

            counts[severity] += 1

        return counts

    left_counts = severity_counts(left.get("findings", []))
    right_counts = severity_counts(right.get("findings", []))

    c1, c2, c3, c4 = st.columns(4)

    for col, level in zip((c1, c2, c3, c4), ("CRITICAL", "HIGH", "MEDIUM", "LOW")):

        col.metric(
            level.title(),
            right_counts[level],
            delta=right_counts[level] - left_counts[level],
            delta_color="inverse"
        )

    st.divider()

    st.subheader("New Findings in Compared Scan")

    def finding_key(finding):

        return (
            finding.get("type") or finding.get("category") or "",
            finding.get("description", "")
        )

    left_keys = {finding_key(f) for f in left.get("findings", [])}
    right_findings = right.get("findings", [])

    new_findings = [
        f for f in right_findings
        if finding_key(f) not in left_keys
    ]

    if not new_findings:
        st.success("No new findings compared to the baseline scan.")
    else:

        for finding in new_findings:

            severity = str(finding.get("severity", "LOW")).upper()
            title = finding.get("type") or finding.get("category") or "Finding"
            description = finding.get("description", "")

            st.warning(f"**{severity} · {title}**\n\n{description}")

    st.subheader("Resolved Findings")

    right_keys = {finding_key(f) for f in right_findings}
    left_findings = left.get("findings", [])

    resolved_findings = [
        f for f in left_findings
        if finding_key(f) not in right_keys
    ]

    if not resolved_findings:
        st.info("No findings were resolved compared to the baseline scan.")
    else:

        for finding in resolved_findings:

            severity = str(finding.get("severity", "LOW")).upper()
            title = finding.get("type") or finding.get("category") or "Finding"
            description = finding.get("description", "")

            st.success(f"**{severity} · {title}**\n\n{description}")