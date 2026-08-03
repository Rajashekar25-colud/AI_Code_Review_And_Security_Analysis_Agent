import os

from tools.bandit_runner import BanditRunner
from tools.spotbugs_runner import SpotBugsRunner
from tools.java_security_scanner import JavaSecurityScanner


class SecurityAgent:
    """
    Security Vulnerability Agent

    Performs security analysis for Python and Java code.
    Uses:
    - Bandit for Python security analysis
    - Java Security Scanner for Java source analysis
    - SpotBugs for compiled Java analysis
    """

    def __init__(self):

        # Python security analyzer
        self.bandit = BanditRunner()


        # Java source code analyzer
        self.java_scanner = JavaSecurityScanner()


        # Java bytecode analyzer (optional)
        self.spotbugs = SpotBugsRunner(
            spotbugs_path=os.getenv(
                "SPOTBUGS_PATH"
            ),
            plugin_path=os.getenv(
                "FINDSECBUGS_PLUGIN"
            )
        )


    def analyze(
        self,
        code,
        language,
        class_directory=None
    ):

        findings = []


        if not code:
            return {
                "agent": "Security Vulnerability Agent",
                "language": language,
                "findings": findings
            }


        language = language.lower()


        # Python security analysis
        if language == "python":

            findings.extend(
                self.bandit.run(code)
            )


        # Java security analysis
        elif language == "java":

            # Source-level security checks
            findings.extend(
                self.java_scanner.run(code)
            )


            # Bytecode-level security checks
            if class_directory:

                findings.extend(
                    self.spotbugs.run(
                        class_directory
                    )
                )


        return {

            "agent":
            "Security Vulnerability Agent",

            "language":
            language,

            "findings":
            findings

        }