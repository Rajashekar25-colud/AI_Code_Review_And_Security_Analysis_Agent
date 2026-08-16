"""
Single source of truth for turning a findings list into a 0-100
score. Used by both database/repository.py (persisted scores) and
ui/dashboard.py (live display), so a review's score is guaranteed
to match everywhere it's shown.
"""

from modules.severity import get_severity_weights


def calculate_score(findings: list) -> int:
    """
    Deduction model: start at 100, subtract each finding's
    severity weight (from config/severity_weights.json), floor
    at 0.
    """

    weights = get_severity_weights()

    penalty = 0

    for finding in findings:
        severity = str(finding.get("severity", "LOW")).upper()
        penalty += weights.get(severity, 1)

    return max(0, 100 - penalty)