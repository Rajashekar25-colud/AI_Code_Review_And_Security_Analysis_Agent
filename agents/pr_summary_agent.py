from langchain_core.messages import HumanMessage

from rag.groq_model import get_groq_model


class PRSummaryAgent:
    """
    Generates a concise professional Pull Request Summary.

    Uses only static analysis findings.
    Avoids sending source code and remediation details
    to reduce LLM token usage.
    """

    def __init__(self):

        self.llm = get_groq_model(
            temperature=0.2
        )


    def generate_summary(
        self,
        source_code,
        language,
        findings,
        remediation=None
    ):
        """
        Generate PR summary from analysis findings.

        source_code and remediation are kept for
        compatibility with existing LangGraph workflow.
        """

        if not findings:

            return {
                "agent": "PR Summary Agent",
                "summary":
                    "No security or quality issues were detected. "
                    "The submitted code passed the current analysis checks."
            }


        prompt = self._build_prompt(
            language,
            findings
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
                "agent": "PR Summary Agent",
                "summary": response.content
            }


        except Exception as e:

            return {
                "agent": "PR Summary Agent",
                "summary":
                    "PR summary generation failed.",
                "error": str(e)
            }



    def _build_prompt(
        self,
        language,
        findings
    ):

        # Prevent huge prompts
        findings_text = str(findings)

        if len(findings_text) > 4000:
            findings_text = findings_text[:4000]


        return f"""
You are a Senior Software Architect reviewing a Pull Request.

Programming Language:
{language}


Static Analysis Findings:
{findings_text}


Generate a concise professional GitHub Pull Request review.


Use exactly these sections:


1. Executive Summary

Summarize the overall purpose and detected issues.


2. Overall Code Health

Describe the current quality and security status.


3. Severity Breakdown

Mention only severity counts present in findings.


4. Important Findings

List the important detected issues.


5. Recommended Priority

Explain which issues should be fixed first.


6. Positive Observations

Mention good practices found in the code.


7. Final Recommendation

Give approve/reject recommendation based only on findings.


Rules:

- Use ONLY provided findings.
- Do NOT invent vulnerabilities.
- Do NOT invent severity numbers.
- Do NOT include corrected code.
- Do NOT include OWASP explanations.
- Do NOT include remediation steps.
- Keep response below 300 words.
- Write like a professional GitHub code reviewer.
"""