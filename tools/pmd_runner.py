import json
import os
import subprocess
import tempfile


class PMDRunner:
    """
    Executes PMD for Java static code analysis.
    """

    def __init__(
        self,
        pmd_path,
        ruleset="category/java/bestpractices.xml"
    ):
        self.pmd_path = pmd_path
        self.ruleset = ruleset

    def run(self, code):

        findings = []

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".java",
            delete=False,
            mode="w",
            encoding="utf-8"
        )

        try:

            temp_file.write(code)
            temp_file.close()

            command = [
                self.pmd_path,
                "check",
                "-d",
                temp_file.name,
                "-R",
                self.ruleset,
                "-f",
                "json"
            ]

            creationflags = 0
            if os.name == "nt":
                creationflags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                creationflags=creationflags
            )

            # PMD returns:
            # 0 -> No violations
            # 4 -> Violations found
            if result.returncode not in (0, 4):
                return findings

            if not result.stdout.strip():
                return findings

            try:
                report = json.loads(result.stdout)
            except json.JSONDecodeError:
                return findings

            for file_data in report.get("files", []):

                for issue in file_data.get("violations", []):

                    priority = int(
                        issue.get("priority", 5)
                    )

                    if priority == 1:
                        severity = "CRITICAL"
                    elif priority == 2:
                        severity = "HIGH"
                    elif priority == 3:
                        severity = "MEDIUM"
                    else:
                        severity = "LOW"

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "tool": "PMD",
                            "type": issue.get("rule", "PMD"),
                            "severity": severity,
                            "line": issue.get("beginLine", 0),
                            "description": issue.get("description", ""),
                            "recommendation": (
                                f"Follow PMD rule: "
                                f"{issue.get('rule', '')}"
                            )
                        }
                    )

        except Exception:
            return findings

        finally:

            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

        return findings