from langchain_core.messages import HumanMessage

from rag.groq_model import get_groq_model
from modules.severity import format_findings_for_prompt


class RemediationAgent:
    """
    Generates AI-powered remediation suggestions
    for code review findings.

    Optimized for Groq token limits.
    """

    def __init__(self):

        # Prompt asks for up to 700 words plus code examples -
        # 512 tokens (the old shared default) wasn't enough and
        # was truncating reports mid-example.
        self.llm = get_groq_model(
            temperature=0.2,
            max_tokens=1536
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

        # Explicit "[SEVERITY] Title - Description" format, sorted
        # CRITICAL first - far less ambiguous for the LLM to parse
        # than a raw Python dict repr, and less likely to cause it
        # to invent or recalculate a severity.
        findings_text = format_findings_for_prompt(findings)


        return f"""
You are a Senior Secure Software Engineer.

Generate a concise remediation report.

Programming Language:
{language}


Security Findings (already severity-classified - copy each
finding's [SEVERITY] EXACTLY as shown, do not recalculate,
reinterpret, or invent a different severity for any finding):

{findings_text}


For each finding include:

1. Issue Name

2. Risk Explanation

3. Severity (copy exactly from the bracketed tag above)

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