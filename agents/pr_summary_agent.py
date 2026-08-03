import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


class PRSummaryAgent:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2
        )


    def generate_summary(
            self,
            source_code,
            language,
            findings,
            remediation
    ):

        if not findings:

            return {
                "agent": "PR Summary Agent",
                "summary": "No issues were detected."
            }


        prompt = self._build_prompt(
            source_code,
            language,
            findings,
            remediation
        )


        response = self.llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )


        return {
            "agent": "PR Summary Agent",
            "summary": response.content
        }



    def _build_prompt(
            self,
            source_code,
            language,
            findings,
            remediation
    ):

        prompt = f"""
You are a Senior Software Architect performing a Pull Request review.

Create a professional code review summary.

Include:

1. Executive Summary
2. Overall Code Health
3. Severity Breakdown
4. Important Findings
5. Recommended Priority
6. Positive Observations
7. Final Recommendation


Rules:

- Use only the provided analysis results.
- Do not invent issues.
- Do not invent severity counts.
- Give recommendations based on findings.


Programming Language:

{language}


Static Analysis Findings:

{findings}


Remediation Suggestions:

{remediation}


Source Code:

{source_code}


Generate the Pull Request review summary.
"""

        return prompt