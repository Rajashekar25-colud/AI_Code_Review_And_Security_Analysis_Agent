import json
import os
import re


CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "java_quality_severity.json"
)

_severity_map = None


def _load_severity_map():

    global _severity_map

    if _severity_map is None:

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _severity_map = json.load(f)

    return _severity_map


class JavaQualityAnalyzer:
    """
    Custom Java code quality analyzer.

    Detects:
    - Unused local variables
    - Empty catch blocks
    """

    def analyze(self, code):

        findings = []

        findings.extend(
            self.detect_unused_variables(code)
        )

        findings.extend(
            self.detect_empty_catch(code)
        )

        return findings

    def detect_unused_variables(self, code):

        findings = []

        variables = re.findall(
            r'\b(int|String|double|float|boolean|char)\s+(\w+)\s*=',
            code
        )

        severity = _load_severity_map().get(
            "unused_local_variable",
            "LOW"
        )

        for datatype, variable in variables:

            count = code.count(variable)

            if count == 1:

                findings.append(
                    {
                        "issue": "Unused Local Variable",
                        "severity": severity,
                        "description":
                        f"Variable '{variable}' is declared but never used.",
                        "recommendation":
                        "Remove unused variables to improve readability and maintainability."
                    }
                )

        return findings

    def detect_empty_catch(self, code):

        findings = []

        pattern = r'catch\s*\([^)]*\)\s*\{\s*\}'

        matches = re.findall(
            pattern,
            code
        )

        severity = _load_severity_map().get(
            "empty_catch_block",
            "LOW"
        )

        if matches:

            findings.append(
                {
                    "issue": "Empty Catch Block",
                    "severity": severity,
                    "description":
                    "Exception is caught but not handled.",
                    "recommendation":
                    "Handle exceptions properly or log the error."
                }
            )

        return findings