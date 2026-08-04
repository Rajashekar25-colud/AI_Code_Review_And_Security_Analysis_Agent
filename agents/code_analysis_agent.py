import os
import stat
from pathlib import Path

from tools.pylint_runner import PylintRunner
from tools.radon_runner import RadonRunner
from tools.pmd_runner import PMDRunner
from tools.checkstyle_runner import CheckstyleRunner
from tools.java_quality_analyzer import JavaQualityAnalyzer


class CodeAnalysisAgent:
    """
    Performs static code quality analysis using
    language-specific analysis tools.

    Python:
        - Pylint
        - Radon

    Java:
        - PMD
        - Checkstyle
        - Custom Java Quality Analyzer
    """

    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent
        tools_dir = base_dir / "tools"


        # ----------------------------
        # PMD
        # ----------------------------

        pmd_home = os.getenv(
            "PMD_HOME",
            str(tools_dir / "pmd-bin-7.26.0")
        )

        pmd_home = Path(pmd_home)

        if os.name == "nt":

            pmd_binary = (
                pmd_home /
                "bin" /
                "pmd.bat"
            )

        else:

            pmd_binary = (
                pmd_home /
                "bin" /
                "pmd"
            )

            if pmd_binary.exists():

                mode = pmd_binary.stat().st_mode

                pmd_binary.chmod(
                    mode
                    | stat.S_IXUSR
                    | stat.S_IXGRP
                    | stat.S_IXOTH
                )


        # ----------------------------
        # Checkstyle
        # ----------------------------

        checkstyle_jar = Path(
            os.getenv(
                "CHECKSTYLE_JAR",
                str(
                    tools_dir /
                    "checkstyle-13.9.0-all.jar"
                )
            )
        )


        checkstyle_config = Path(
            os.getenv(
                "CHECKSTYLE_CONFIG",
                str(
                    tools_dir /
                    "sun_checks.xml"
                )
            )
        )


        # ----------------------------
        # Analysis Tools
        # ----------------------------

        self.pylint = PylintRunner()

        self.radon = RadonRunner()

        self.pmd = PMDRunner(
            pmd_path=str(pmd_binary)
        )

        self.checkstyle = CheckstyleRunner(
            jar_path=str(checkstyle_jar),
            config_path=str(checkstyle_config)
        )


        # Custom Java quality rules
        self.java_quality = JavaQualityAnalyzer()



    def analyze(self, code, language):

        findings = []

        language = language.lower()


        if language == "python":

            findings.extend(
                self.pylint.run(code)
            )

            findings.extend(
                self.radon.run(code)
            )


        elif language == "java":

            findings.extend(
                self.pmd.run(code)
            )

            findings.extend(
                self.checkstyle.run(code)
            )

            findings.extend(
                self.java_quality.analyze(code)
            )


        return {
            "agent": "Code Analysis Agent",
            "language": language,
            "findings": findings
        }