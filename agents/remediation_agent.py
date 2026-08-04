from langchain_core.messages import HumanMessage

from rag.groq_model import get_groq_model


class RemediationAgent:
    """
    Generates AI-powered remediation suggestions
    for code review findings.

    Optimized for Groq token limits.
    """

    def __init__(self):

        self.llm = get_groq_model(
            temperature=0.2
        )


    def generate(
        self,
        findings,
        source_code,
        language=None
    ):

        if not findings:

            return {
                "agent": "Remediation Agent",
                "recommendations": [
                    {
                        "summary": "No issues detected.",
                        "corrected_code": source_code
                    }
                ]
            }


        prompt = self._build_prompt(
            findings,
            language
        )


        try:

            response = self.llm.invoke(
                [
                    HumanMessage(
                        content=prompt
                    )
                ]
            )


            return {
                "agent": "Remediation Agent",
                "recommendations": response.content
            }


        except Exception as e:

            return {
                "agent": "Remediation Agent",
                "error": str(e)
            }



    def _build_prompt(
        self,
        findings,
        language=None
    ):

        findings_text = str(findings)


        # Limit input size to avoid Groq 413 error
        if len(findings_text) > 5000:
            findings_text = findings_text[:5000]


        return f"""
You are a Senior Secure Software Engineer.

Generate a concise remediation report.

Programming Language:
{language}


Security Findings:

{findings_text}


For each finding include:

1. Issue Name

2. Risk Explanation

3. Severity

4. Recommended Fix

5. Secure Coding Practice

6. Short Corrected Code Example


Rules:

- Use only provided findings.
- Do not invent vulnerabilities.
- Do not analyze unavailable code.
- Do not include OWASP explanations.
- Do not include long documentation.
- Never create real secrets.
- Never include API keys/passwords/tokens.
- Use placeholders for sensitive values.
- Keep response below 700 words.

Generate the remediation report.
"""