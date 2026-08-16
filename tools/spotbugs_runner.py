import json
import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET


CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "spotbugs_priority_map.json"
)

_priority_map = None


def _load_priority_map():

    global _priority_map

    if _priority_map is None:

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            _priority_map = json.load(f)

    return _priority_map


class SpotBugsRunner:

    def __init__(
        self,
        spotbugs_path,
        plugin_path=None
    ):

        self.spotbugs_path = spotbugs_path
        self.plugin_path = plugin_path

    def run(self, class_directory):

        findings = []

        if (
            not class_directory
            or not os.path.exists(class_directory)
        ):
            return findings

        report_file = tempfile.NamedTemporaryFile(
            suffix=".xml",
            delete=False
        )

        report_file.close()

        try:

            command = [
                self.spotbugs_path,
                "-textui",
                "-xml:withMessages",
                "-output",
                report_file.name
            ]

            if self.plugin_path and os.path.exists(self.plugin_path):

                command.extend(
                    [
                        "-pluginList",
                        self.plugin_path
                    ]
                )

            command.append(
                class_directory
            )

            creationflags = 0
            if os.name == "nt":
                creationflags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                creationflags=creationflags
            )

            if result.returncode not in (0, 1):
                return findings

            if (
                not os.path.exists(report_file.name)
                or os.path.getsize(report_file.name) == 0
            ):
                return findings

            tree = ET.parse(
                report_file.name
            )

            root = tree.getroot()

            for bug in root.findall(
                "BugInstance"
            ):

                source = bug.find(
                    "SourceLine"
                )

                message = bug.find(
                    "LongMessage"
                )

                priority = bug.attrib.get(
                    "priority",
                    "3"
                )

                severity = _load_priority_map().get(
                    priority,
                    "LOW"
                )

                findings.append(
                    {
                        "agent": "Security Vulnerability Agent",
                        "tool": "SpotBugs",
                        "type": bug.attrib.get(
                            "type",
                            "Unknown"
                        ),
                        "severity": severity,
                        "line": int(
                            source.attrib.get(
                                "start",
                                0
                            )
                        )
                        if source is not None
                        else 0,
                        "description": message.text
                        if message is not None
                        else "",
                        "recommendation":
                        "Follow the security recommendation provided by the analysis tool."
                    }
                )

        except Exception:
            return findings

        finally:

            if os.path.exists(
                report_file.name
            ):

                os.remove(
                    report_file.name
                )

        return findings