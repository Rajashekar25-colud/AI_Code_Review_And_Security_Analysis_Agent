import json
import os
import subprocess
import tempfile


class BanditRunner:
    """
    Executes Bandit for Python security analysis.
    No security rules are implemented manually.
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
                "bandit",
                "-f",
                "json",
                temp_file.name
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            report = json.loads(result.stdout)

            for issue in report.get("results", []):

                findings.append(
                    {
                        "agent": "Security Agent",
                        "tool": "Bandit",
                        "test_id": issue.get("test_id"),
                        "test_name": issue.get("test_name"),
                        "issue_text": issue.get("issue_text"),
                        "severity": issue.get("issue_severity"),
                        "confidence": issue.get("issue_confidence"),
                        "line": issue.get("line_number"),
                        "file": issue.get("filename"),
                        "code": issue.get("code"),
                        "more_info": issue.get("more_info")
                    }
                )

        except Exception as e:

            findings.append(
                {
                    "agent": "Security Agent",
                    "tool": "Bandit",
                    "error": str(e)
                }
            )

        finally:

            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

        return findings