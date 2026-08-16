"""
Unit tests for modules/severity.py and modules/score_calculator.py.

These tests only exercise pure functions backed by config/*.json —
no LLM calls, no external tool subprocess calls, no database — so
they run anywhere without API keys or Java/PMD/SpotBugs installed.
"""

import sys
import os

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from modules.severity import (
    normalize_severity,
    normalize_findings,
    tag_owasp_category,
    get_severity_weights
)
from modules.score_calculator import calculate_score


def test_normalize_severity_trusts_native_value():

    finding = {"type": "Anything", "severity": "high"}

    assert normalize_severity(finding) == "HIGH"


def test_normalize_severity_falls_back_to_category_map():

    finding = {"type": "SQL Injection"}

    assert normalize_severity(finding) == "CRITICAL"


def test_normalize_severity_defaults_to_low():

    finding = {"type": "Some Unknown Thing"}

    assert normalize_severity(finding) == "LOW"


def test_normalize_findings_adds_severity_and_owasp():

    findings = [
        {"type": "SQL Injection"},
        {"type": "Hardcoded Secret"}
    ]

    result = normalize_findings(findings)

    assert result[0]["severity"] == "CRITICAL"
    assert result[0]["owasp_category"] is not None

    assert result[1]["severity"] == "HIGH"


def test_tag_owasp_category_no_match_returns_none():

    finding = {"type": "Totally Unrelated Thing"}

    assert tag_owasp_category(finding) is None


def test_get_severity_weights_has_all_four_levels():

    weights = get_severity_weights()

    for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        assert level in weights


def test_calculate_score_no_findings_is_perfect():

    assert calculate_score([]) == 100


def test_calculate_score_decreases_with_findings():

    findings = [{"severity": "CRITICAL"}]

    assert calculate_score(findings) < 100


def test_calculate_score_never_goes_below_zero():

    findings = [{"severity": "CRITICAL"}] * 50

    assert calculate_score(findings) == 0


if __name__ == "__main__":

    import pytest

    pytest.main([__file__, "-v"])