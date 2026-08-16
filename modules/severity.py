"""
Severity normalizer and finding-shape normalizer.

Different tools (Bandit, PMD, SpotBugs, Checkstyle, Pylint, Radon,
Groq) each report severity - and even basic fields like "what is
this issue called" and "what is the description" - in their own
way. This module makes every finding consistent before it reaches
the dashboard, reports, or PDF:

- normalize_severity(): maps to CRITICAL/HIGH/MEDIUM/LOW, using
  config/severity_map.json - not hardcoded in Python.
- normalize_finding_fields(): fills in type/description/
  recommendation from whatever fields a tool actually set (e.g.
  Pylint's "message" becomes "description", Radon's complexity
  numbers become a readable description) - field aliasing, not
  invented content.
- tag_owasp_category(): OWASP Top 10 tagging via
  config/owasp_map.json.
- get_severity_weights(): shared scoring weights for
  database/repository.py and ui/dashboard.py.
"""

import json
import os

CONFIG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config"
)

SEVERITY_MAP_PATH = os.path.join(CONFIG_DIR, "severity_map.json")
SEVERITY_WEIGHTS_PATH = os.path.join(CONFIG_DIR, "severity_weights.json")
OWASP_MAP_PATH = os.path.join(CONFIG_DIR, "owasp_map.json")

_severity_map = None
_severity_weights = None
_owasp_map = None


def _load_map():

    global _severity_map

    if _severity_map is None:

        with open(SEVERITY_MAP_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)

        _severity_map = {key.lower(): value.upper() for key, value in raw.items()}

    return _severity_map


def _load_owasp_map():

    global _owasp_map

    if _owasp_map is None:

        with open(OWASP_MAP_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)

        _owasp_map = {key.lower(): value for key, value in raw.items()}

    return _owasp_map


def get_severity_weights() -> dict:
    """
    Shared severity->penalty weight table, used by both the
    database scoring (database/repository.py) and the dashboard
    (ui/dashboard.py), so a review's score is always computed the
    same way everywhere. Backed by config/severity_weights.json.
    """

    global _severity_weights

    if _severity_weights is None:

        with open(SEVERITY_WEIGHTS_PATH, "r", encoding="utf-8") as f:
            _severity_weights = json.load(f)

    return _severity_weights


def normalize_severity(finding: dict) -> str:
    """
    Returns the standardized severity (CRITICAL / HIGH / MEDIUM / LOW)
    for a single finding.

    Priority order:
    1. The tool's own native severity, if it already reported one
       that matches our 4-level scale.
    2. The category/type keyword lookup in
       config/severity_map.json.
    3. LOW, as a last-resort default.
    """

    existing = str(finding.get("severity", "")).upper()

    is_llm_sourced = finding.get("tool") == "Groq LLM"

    # LLM-reported severity has proven unreliable in testing (it
    # consistently under-reported CRITICAL-tier vulnerabilities as
    # HIGH even when explicitly instructed on the severity
    # standard). For LLM-sourced findings, always fall through to
    # the keyword-based config/severity_map.json lookup below -
    # the same authoritative standard already used for every
    # Python static-analysis finding - instead of trusting the
    # LLM's own self-assessment.
    if existing in ("CRITICAL", "HIGH", "MEDIUM", "LOW") and not is_llm_sourced:
        return existing

    severity_map = _load_map()

    label = (
        finding.get("type")
        or finding.get("category")
        or ""
    ).strip().lower()

    for key, mapped_severity in severity_map.items():

        if key in label:
            return mapped_severity

    return "LOW"


def tag_owasp_category(finding: dict):
    """
    Returns the matching OWASP Top 10 (2021) category for a
    finding, based on config/owasp_map.json. Returns None if no
    keyword matches - not every finding is a security finding.
    """

    owasp_map = _load_owasp_map()

    label = (
        finding.get("type")
        or finding.get("category")
        or finding.get("issue")
        or ""
    ).strip().lower()

    for key, category in owasp_map.items():

        if key in label:
            return category

    return None


def normalize_finding_fields(finding: dict) -> dict:
    """
    Ensures every finding has a usable type/description/
    recommendation, regardless of which tool produced it.

    This is field aliasing - mapping each tool's own field names
    onto the common shape - not invented content. Nothing here
    fabricates a security claim; it only relabels data the tool
    itself already returned (e.g. Pylint's "message" field becomes
    "description", Radon's complexity number becomes a readable
    sentence built from Radon's own numbers).
    """

    updated = dict(finding)

    # ---- type ----
    if not updated.get("type"):

        updated["type"] = (
            updated.get("issue")
            or updated.get("symbol")
            or updated.get("test_name")
            or updated.get("category")
            or updated.get("name")
            or updated.get("title")
            or "Unknown"
        )

    # ---- description ----
    if not updated.get("description"):

        if updated.get("message"):

            updated["description"] = updated["message"]

        elif updated.get("issue_text"):

            updated["description"] = updated["issue_text"]

        elif updated.get("complexity") is not None:

            updated["description"] = (
                f"Cyclomatic complexity of {updated.get('complexity')} "
                f"(rank {updated.get('rank', '?')}) for "
                f"{updated.get('type', 'this block')} "
                f"'{updated.get('name', '')}'."
            )

        else:

            updated["description"] = "No description available"

    # ---- recommendation ----
    if not updated.get("recommendation"):

        tool = updated.get("tool", "")

        if tool == "Radon":

            updated["recommendation"] = (
                "Consider refactoring this function to reduce "
                "cyclomatic complexity."
            )

        elif tool == "Pylint":

            updated["recommendation"] = (
                "Follow the Pylint suggestion to improve code quality."
            )

        else:

            updated["recommendation"] = "No recommendation available"

    return updated


def normalize_findings(findings: list) -> list:
    """
    Returns a new list of findings with each finding's severity,
    type/description/recommendation fields, and OWASP category
    all normalized.
    """

    normalized = []

    for finding in findings:

        updated = normalize_finding_fields(finding)
        updated["severity"] = normalize_severity(updated)
        updated["owasp_category"] = tag_owasp_category(updated)
        normalized.append(updated)

    return normalized


SEVERITY_RANK = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}


def sort_findings_by_severity(findings: list) -> list:
    """
    Returns a new list of findings ordered CRITICAL -> HIGH ->
    MEDIUM -> LOW. Used before truncating findings for an LLM
    prompt (Remediation Agent, PR Summary Agent), so if anything
    gets cut for length, it's the least severe findings - not the
    most severe ones sitting later in the original list order.
    """

    return sorted(
        findings,
        key=lambda f: SEVERITY_RANK.get(
            str(f.get("severity", "LOW")).upper(), 4
        )
    )


MAX_FINDINGS_IN_PROMPT = 10


def format_findings_for_prompt(findings: list) -> str:
    """
    Renders findings as an explicit, numbered "[SEVERITY] Title -
    Description" list for LLM prompts (Remediation Agent, PR
    Summary Agent, Conversational Assistant).

    A clean explicit format like this is far less likely to cause
    the LLM to mis-derive or invent a severity than handing it a
    raw Python dict repr (str(findings)) and asking it to figure
    severity out from context.
    """

    if not findings:
        return "No findings."

    ordered = sort_findings_by_severity(findings)

    lines = []

    for index, finding in enumerate(
        ordered[:MAX_FINDINGS_IN_PROMPT], start=1
    ):

        severity = str(finding.get("severity", "LOW")).upper()
        title = finding.get("type") or finding.get("category") or "Finding"
        description = finding.get("description", "")

        lines.append(f"{index}. [{severity}] {title} - {description}")

    remaining = len(ordered) - MAX_FINDINGS_IN_PROMPT

    if remaining > 0:
        lines.append(f"...and {remaining} more finding(s), omitted here for length.")

    return "\n".join(lines)