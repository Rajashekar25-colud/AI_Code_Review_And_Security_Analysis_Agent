import logging
import os


from tools.bandit_runner import BanditRunner
from tools.spotbugs_runner import SpotBugsRunner
from tools.java_security_scanner import JavaSecurityScanner

from agents.java_security_analyzer import JavaSecurityAnalyzer

logger = logging.getLogger(__name__)


SUPPORTED_LANGUAGES = {
    "python",
    "java"
}



class SecurityAgent:
    """
    Security Vulnerability Agent

    Responsibilities:

    Python:
        - Bandit security analysis

    Java:
        - Java AST extraction
        - OWASP RAG + Groq vulnerability analysis
        - SpotBugs bytecode analysis

    No vulnerability knowledge is hardcoded.
    """


    def __init__(self):


        # -----------------------------
        # Python Analyzer
        # -----------------------------

        self.bandit = BanditRunner()



        # -----------------------------
        # Java AST Analyzer
        # -----------------------------

        self.java_scanner = JavaSecurityScanner()



        # -----------------------------
        # Java AI Security Analyzer
        # RAG + Groq
        # -----------------------------

        self.java_ai_analyzer = (
            JavaSecurityAnalyzer()
        )



        # -----------------------------
        # Java Bytecode Analyzer
        # -----------------------------

        self.spotbugs = SpotBugsRunner(

            spotbugs_path=os.getenv(
                "SPOTBUGS_PATH"
            ),

            plugin_path=os.getenv(
                "FINDSECBUGS_PLUGIN"
            )

        )




    def _run_tool(
        self,
        tool_name,
        function,
        *args,
        **kwargs
    ):

        """
        Executes security tools safely.

        One tool failure should not
        stop complete review pipeline.
        """


        try:


            result = function(
                *args,
                **kwargs
            )


            return result or []



        except Exception as error:


            logger.exception(
                "%s failed",
                tool_name
            )


            return [

                {

                    "title":
                    "Security Tool Failure",


                    "tool":
                    tool_name,


                    "severity":
                    "info",


                    "category":
                    "system",


                    "description":
                    str(error),


                    "recommendation":
                    "Check tool configuration."

                }

            ]






    def analyze(
        self,
        code,
        language,
        class_directory=None
    ):


        findings = []



        if not code:


            return {

                "agent":
                "Security Vulnerability Agent",


                "language":
                language,


                "findings":
                []

            }




        language = (
            language or ""
        ).lower()



        if language not in SUPPORTED_LANGUAGES:


            return {


                "agent":
                "Security Vulnerability Agent",


                "language":
                language,


                "findings":
                [],


                "status":
                "unsupported_language"

            }




        # ==================================================
        # PYTHON SECURITY ANALYSIS
        # ==================================================

        if language == "python":


            python_findings = self._run_tool(

                "bandit",

                self.bandit.run,

                code

            )


            findings.extend(
                python_findings
            )




        # ==================================================
        # JAVA SECURITY ANALYSIS
        # ==================================================

        elif language == "java":



            # --------------------------------------
            # Step 1
            # Java AST Extraction
            # --------------------------------------

            java_ast = self._run_tool(

                "java_security_scanner",

                self.java_scanner.run,

                code

            )




            # --------------------------------------
            # Step 2
            # OWASP RAG + Groq Analysis
            # --------------------------------------

            java_security_findings = (
                self._run_tool(

                    "java_ai_security_analyzer",

                    self.java_ai_analyzer.analyze,

                    code

                )
            )



            findings.extend(
                java_security_findings
            )




            # --------------------------------------
            # Step 3
            # SpotBugs Analysis
            # --------------------------------------

            if class_directory:


                spotbugs_findings = self._run_tool(

                    "spotbugs",

                    self.spotbugs.run,

                    class_directory

                )


                findings.extend(
                    spotbugs_findings
                )





            return {


                "agent":
                "Security Vulnerability Agent",


                "language":
                "java",


                "findings":
                findings,


                "java_ast":
                java_ast,


                "status":
                "completed"

            }





        return {


            "agent":
            "Security Vulnerability Agent",


            "language":
            language,


            "findings":
            findings,


            "status":
            "completed"

        }