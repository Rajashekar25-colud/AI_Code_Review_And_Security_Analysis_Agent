import json
import logging

from rag.groq_model import get_groq_model
from rag.embedding import get_embedding_model
from rag.vector_store import load_vector_store


logger = logging.getLogger(__name__)


class JavaSecurityAnalyzer:
    """
    Java Security Analyzer

    Uses:
    - Java AST information
    - RAG Knowledge Base
    - Groq LLM

    Detects OWASP security issues.
    """

    def __init__(self):

        self.llm = get_groq_model()

        self.embedding_model = get_embedding_model()

        self.vector_store = load_vector_store(
            self.embedding_model
        )


    def analyze(self, java_code):

        try:

            documents = self.vector_store.similarity_search(
                java_code,
                k=3
            )


            context = "\n".join(
                doc.page_content
                for doc in documents
            )


            prompt = f"""
You are a Java Security Expert.

Analyze this Java code.

Detect only real vulnerabilities:

- SQL Injection
- Insecure Deserialization
- Hardcoded Secrets
- Weak Authentication
- Broken Access Control
- XSS
- Command Injection

Return ONLY JSON.

Format:

[
 {{
 "issue": "",
 "severity": "",
 "description": "",
 "recommendation": "",
 "secure_code": ""
 }}
]


Java Code:

{java_code}


Security Knowledge:

{context}

"""


            response = self.llm.invoke(prompt)


            content = response.content


            content = (
                content
                .replace("```json","")
                .replace("```","")
                .strip()
            )


            return json.loads(content)


        except Exception as e:

            logger.error(
                "Java security analysis failed: %s",
                e
            )

            return [
                {
                    "issue": "Analyzer Error",
                    "severity": "Info",
                    "description": str(e),
                    "recommendation": "",
                    "secure_code": ""
                }
            ]