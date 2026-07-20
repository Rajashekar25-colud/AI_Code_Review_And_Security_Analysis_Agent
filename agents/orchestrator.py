from agents.code_analysis_agent import CodeAnalysisAgent
from agents.security_agent import SecurityAgent


class Orchestrator:

    def __init__(self):

        self.code_agent = CodeAnalysisAgent()

        self.security_agent = SecurityAgent()



    def analyze_code(self, code, language):

        code_result = self.code_agent.analyze(
            code,
            language
        )


        security_result = self.security_agent.analyze(
            code,
            language
        )


        all_findings = (
            code_result["findings"]
            +
            security_result["findings"]
        )


        summary = self.generate_summary(
            all_findings
        )


        return {
            "summary": summary,
            "findings": all_findings
        }



    def generate_summary(self, findings):

        summary = {

            "CRITICAL": 0,

            "HIGH": 0,

            "MEDIUM": 0,

            "LOW": 0
        }


        for finding in findings:

            severity = finding.get(
                "severity",
                "LOW"
            ).upper()


            if severity in summary:

                summary[severity] += 1


        return summary