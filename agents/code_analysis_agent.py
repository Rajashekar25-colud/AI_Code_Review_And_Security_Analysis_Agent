from tools.pylint_runner import PylintRunner
from tools.radon_runner import RadonRunner
from tools.pmd_runner import PMDRunner
from tools.checkstyle_runner import CheckstyleRunner


class CodeAnalysisAgent:
    """
    Performs static code quality analysis using
    language-specific analysis tools.
    """

    def __init__(self):

        self.pylint = PylintRunner()

        self.radon = RadonRunner()

        self.pmd = PMDRunner(
            pmd_path="tools/pmd-bin-7.26.0/bin/pmd.bat"
        )

        self.checkstyle = CheckstyleRunner(
            jar_path="tools/checkstyle-13.9.0-all.jar",
            config_path="tools/sun_checks.xml"
        )


    def analyze(self, code, language):

        findings = []


        if language == "Python":

            findings.extend(
                self.pylint.run(code)
            )

            findings.extend(
                self.radon.run(code)
            )


        elif language == "Java":

            findings.extend(
                self.pmd.run(code)
            )

            findings.extend(
                self.checkstyle.run(code)
            )


        return {
            "agent": "Code Analysis Agent",
            "language": language,
            "findings": findings
        }