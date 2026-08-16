"""
End-to-end pipeline test — runs actual source code through the
full multi-agent Orchestrator (Code Analysis + Security agents in
parallel, merge, remediation, PR summary).

Requires GROQ_API_KEY (the agents call the Groq LLM) and, for the
Java case, a working PMD/SpotBugs/Checkstyle install. Tests
auto-skip when GROQ_API_KEY isn't set rather than failing, since
this is an integration test, not a unit test.
"""

import sys
import os

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pytest
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY_MISSING = not os.getenv("GROQ_API_KEY")


VULNERABLE_PYTHON_CODE = """
import sqlite3

def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

API_KEY = "sk-hardcoded-secret-key-12345"
"""


CLEAN_PYTHON_CODE = """
def add(a, b):
    return a + b


def multiply(a, b):
    return a * b
"""


@pytest.fixture
def orchestrator():
    from agents.orchestrator import Orchestrator
    return Orchestrator()


@pytest.mark.skipif(
    GROQ_KEY_MISSING,
    reason="GROQ_API_KEY not set - skipping live pipeline test"
)
def test_pipeline_returns_expected_shape(orchestrator):

    result = orchestrator.analyze_code(VULNERABLE_PYTHON_CODE, "Python")

    assert "findings" in result
    assert "remediation" in result
    assert "pr_summary" in result
    assert isinstance(result["findings"], list)


@pytest.mark.skipif(
    GROQ_KEY_MISSING,
    reason="GROQ_API_KEY not set - skipping live pipeline test"
)
def test_pipeline_detects_sql_injection(orchestrator):

    result = orchestrator.analyze_code(VULNERABLE_PYTHON_CODE, "Python")
    findings = result["findings"]

    assert len(findings) > 0

    labels = " ".join(
        (f.get("type") or f.get("category") or "").lower()
        for f in findings
    )

    assert "sql" in labels or "injection" in labels


@pytest.mark.skipif(
    GROQ_KEY_MISSING,
    reason="GROQ_API_KEY not set - skipping live pipeline test"
)
def test_pipeline_detects_hardcoded_secret(orchestrator):

    result = orchestrator.analyze_code(VULNERABLE_PYTHON_CODE, "Python")
    findings = result["findings"]

    labels = " ".join(
        (f.get("type") or f.get("category") or "").lower()
        for f in findings
    )

    assert "secret" in labels or "hardcoded" in labels or "credential" in labels


@pytest.mark.skipif(
    GROQ_KEY_MISSING,
    reason="GROQ_API_KEY not set - skipping live pipeline test"
)
def test_pipeline_every_finding_has_normalized_severity(orchestrator):

    result = orchestrator.analyze_code(VULNERABLE_PYTHON_CODE, "Python")

    for finding in result["findings"]:
        assert finding.get("severity") in ("CRITICAL", "HIGH", "MEDIUM", "LOW")


@pytest.mark.skipif(
    GROQ_KEY_MISSING,
    reason="GROQ_API_KEY not set - skipping live pipeline test"
)
def test_pipeline_clean_code_has_fewer_findings_than_vulnerable_code(orchestrator):

    clean_result = orchestrator.analyze_code(CLEAN_PYTHON_CODE, "Python")
    vulnerable_result = orchestrator.analyze_code(VULNERABLE_PYTHON_CODE, "Python")

    assert len(clean_result["findings"]) < len(vulnerable_result["findings"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])