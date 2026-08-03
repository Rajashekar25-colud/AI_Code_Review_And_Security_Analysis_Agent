import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


class RemediationAgent:

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.environ["GROQ_API_KEY"],
            temperature=0.2
        )


    def generate(self, findings, source_code, language=None):

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
            source_code,
            language
        )


        response = self.llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )


        return {
            "agent": "Remediation Agent",
            "recommendations": response.content
        }



    def _build_prompt(self, findings, source_code, language=None):

        prompt = f"""
You are a Senior Secure Software Engineer.

Your task is to provide remediation guidance for the
following code review findings.

Programming Language:
{language}


For every finding provide:

1. Issue Name

2. Security/Quality Risk Explanation

3. Severity Level

4. Recommended Fix

5. Secure Coding Best Practice

6. Corrected Code Example


Important Rules:

- Do not create hardcoded credentials, API keys, passwords, tokens, or secrets.
- Do not hardcode user-specific values.
- Use environment variables or secure configuration methods.
- Keep the same programming language as the submitted code.
- Use placeholders where sensitive values are required.
- Follow OWASP Secure Coding Guidelines.
- Provide practical developer-friendly fixes.


Code Review Findings:

{findings}


Original Source Code:

{source_code}


Generate a detailed remediation report.
"""


        return prompt