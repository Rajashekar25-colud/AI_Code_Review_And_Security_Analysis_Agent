import json
import os
import subprocess
import tempfile


CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "pylint_severity_map.json"
)

_severity_map = None


def _load_severity_map():

    global _severity_map

    if _severity_map is None:

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _severity_map = json.load(f)

    return _severity_map


class PylintRunner:
    """
    Executes Pylint and returns the reported findings.
    No analysis rules are implemented here.
    """

    def __init__(self):
        pass

    def run(self, code):

        findings = []

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".py",
            delete=False,
            mode="w",
            encoding="utf-8"
        )

        try:

            temp_file.write(code)
            temp_file.close()

            command = [
                "pylint",
                temp_file.name,
                "--output-format=json",
                "--score=n"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.stdout.strip():

                issues = json.loads(result.stdout)

                for issue in issues:

                    pylint_type = issue.get("type", "convention")

                    severity = _load_severity_map().get(
                        pylint_type,
                        "LOW"
                    )

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "tool": "Pylint",
                            "message_id": issue.get("message-id"),
                            "symbol": issue.get("symbol"),
                            "category": pylint_type,
                            "severity": severity,
                            "message": issue.get("message"),
                            "path": issue.get("path"),
                            "module": issue.get("module"),
                            "object": issue.get("object"),
                            "line": issue.get("line"),
                            "column": issue.get("column"),
                            "end_line": issue.get("endLine"),
                            "end_column": issue.get("endColumn")
                        }
                    )

        except Exception as e:

            findings.append(
                {
                    "agent": "Code Analysis Agent",
                    "tool": "Pylint",
                    "error": str(e)
                }
            )

        finally:

            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

        return findings