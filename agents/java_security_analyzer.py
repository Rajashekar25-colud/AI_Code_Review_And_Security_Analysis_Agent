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

        # Needs a larger token budget than the default: this
        # agent returns a JSON array with one entry per detected
        # vulnerability, each including a description and
        # recommendation. The previous 512-token default was
        # truncating the JSON mid-string for any file with more
        # than a couple of findings, causing json.loads() to fail.
        self.llm = get_groq_model(
            max_tokens=2048
        )

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
You are a precise Java Security Auditor. You are being evaluated
on accuracy, and false positives are penalized just as heavily as
missed vulnerabilities.

Analyze ONLY the Java code below. Flag a finding ONLY if you can
point to a SPECIFIC line or construct in THIS code that is
actually vulnerable - not a general best-practice suggestion, not
a hypothetical, not something that "could theoretically matter in
some other context."

Vulnerability categories to check for (only if concretely present):

- SQL Injection: string concatenation/formatting building a SQL
  query with untrusted input.
- Command Injection: Runtime.exec/ProcessBuilder built from
  untrusted input.
- Insecure Deserialization: ObjectInputStream.readObject() on
  data that could come from an untrusted source.
- Hardcoded Secrets: an actual literal password/API key/token
  string assigned to a variable.
- Weak Cryptography: MD5/SHA1/DES used for security purposes.
- Weak Authentication: a login/auth check comparing plaintext
  credentials, or missing entirely where the code's purpose is
  clearly to perform authentication.
- Broken Access Control: a file/resource permission explicitly
  set to world-readable/writable, or an authorization check that
  is present but bypassable.
- Path Traversal: a file path built by concatenating untrusted
  input without validation.
- XSS: untrusted input written directly into an HTML response.

Severity classification - use EXACTLY this standard (matching
the same standard applied to Python findings elsewhere in this
platform), so severity is consistent across languages:

- CRITICAL: SQL Injection, Command Injection, Remote Code
  Execution, Insecure Deserialization, Authentication Bypass
  (a complete absence of any auth check where one is clearly
  required, not merely "weak" auth).
- HIGH: Broken Access Control, SSRF, Hardcoded Secrets, Weak
  Cryptography (MD5/SHA1), XSS, Path Traversal, Weak
  Authentication (auth exists but is flawed, e.g. plaintext
  comparison).
- MEDIUM: CSRF, Information Disclosure.
- LOW: Logging issues, minor style/naming issues.

Do not default everything to HIGH - if a finding genuinely
matches one of the CRITICAL categories above, mark it CRITICAL.

Explicitly do NOT flag:

- Public methods on a utility/helper class - that is normal,
  correct Java design, not "Broken Access Control."
- A class simply not implementing authentication, when nothing
  about its purpose suggests it should (e.g. a math/list/string
  utility class).
- Generic style or design suggestions with no concrete security
  impact.

If the code has no genuine vulnerability from the list above,
return an empty JSON array: []. An empty result is a CORRECT and
EXPECTED outcome for well-written code - do not invent a finding
just to have something to report.

Return ONLY JSON, no prose before or after it.

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

Keep each "description" and "recommendation" to one or two
sentences, so the full JSON response stays well within your
output length limit and is never cut off mid-string.


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


            parsed = json.loads(content)

            # Tag every finding as LLM-sourced, so the severity
            # normalizer knows NOT to blindly trust this LLM's own
            # self-reported severity word (which has proven
            # inconsistent - e.g. always saying HIGH even for
            # textbook SQL Injection) and instead applies the same
            # keyword-based severity standard used for Python
            # findings (config/severity_map.json).
            for finding in parsed:
                finding["tool"] = "Groq LLM"

            return parsed


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