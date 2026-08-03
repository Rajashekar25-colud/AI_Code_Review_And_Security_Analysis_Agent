import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET


class CheckstyleRunner:

    def __init__(self, jar_path, config_path):
        self.jar_path = jar_path
        self.config_path = config_path

    def run(self, code):

        findings = []

        java_file = tempfile.NamedTemporaryFile(
            suffix=".java",
            delete=False,
            mode="w",
            encoding="utf-8"
        )

        report_file = tempfile.NamedTemporaryFile(
            suffix=".xml",
            delete=False
        )

        try:

            java_file.write(code)
            java_file.close()
            report_file.close()

            command = [
                "java",
                "-jar",
                self.jar_path,
                "-c",
                self.config_path,
                "-f",
                "xml",
                "-o",
                report_file.name,
                java_file.name
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if not os.path.exists(report_file.name):
                return []

            if os.path.getsize(report_file.name) == 0:
                return []

            tree = ET.parse(report_file.name)
            root = tree.getroot()

            for file_node in root.findall("file"):

                for error in file_node.findall("error"):

                    severity = error.attrib.get("severity", "info").upper()

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "tool": "Checkstyle",
                            "type": error.attrib.get("source", "").split(".")[-1],
                            "severity": severity,
                            "line": int(error.attrib.get("line", 0)),
                            "description": error.attrib.get("message", ""),
                            "recommendation": "Follow the reported Checkstyle rule."
                        }
                    )

        except Exception as e:

            print("Checkstyle Error:", e)

        finally:

            if os.path.exists(java_file.name):
                os.remove(java_file.name)

            if os.path.exists(report_file.name):
                os.remove(report_file.name)

        return findings