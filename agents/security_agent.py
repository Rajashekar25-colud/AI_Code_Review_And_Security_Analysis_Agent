import re


class SecurityAgent:

    def __init__(self):
        self.findings = []

    def analyze(self, source_code, language):

        self.findings = []

        self._detect_sql_injection(source_code)
        self._detect_hardcoded_secrets(source_code)
        self._detect_weak_passwords(source_code)
        self._detect_eval_usage(source_code)
        self._detect_command_injection(source_code)
        self._detect_weak_crypto(source_code)
        self._detect_xss(source_code)
        self._detect_path_traversal(source_code)
        self._detect_insecure_deserialization(source_code)
        self._detect_weak_random(source_code)
        self._detect_csrf(source_code)
        self._detect_ssrf(source_code)
        self._detect_xxe(source_code)
        self._detect_weak_jwt(source_code)
        self._detect_debug_mode(source_code)

        return {
            "agent": "Security Agent",
            "findings": self.findings
        }

    # =====================================================
    # SQL Injection
    # =====================================================

    def _detect_sql_injection(self, source_code):

        lines = source_code.splitlines()

        full_code = " ".join(lines)

        if re.search(
            r"(SELECT|INSERT|UPDATE|DELETE).*?\+.*",
            full_code,
            re.IGNORECASE
        ):

            self.findings.append(
                {
                    "agent": "Security Agent",
                    "type": "SQL Injection",
                    "severity": "CRITICAL",
                    "line": "Multiple",
                    "description":
                        "SQL query is dynamically created using string concatenation.",
                    "recommendation":
                        "Use PreparedStatement or parameterized queries."
                }
            )

            return

        patterns = [
            r"executeQuery\s*\(",
            r"execute\s*\(",
            r"createStatement\s*\("
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "SQL Injection",
                            "severity": "CRITICAL",
                            "line": line_no,
                            "description":
                                "Possible unsafe SQL execution detected.",
                            "recommendation":
                                "Use parameterized queries."
                        }
                    )

                    break

    # =====================================================
    # Hardcoded Secrets
    # =====================================================

    def _detect_hardcoded_secrets(self, source_code):

        lines = source_code.splitlines()

        pattern = (
            r'(password|passwd|secret|api_key|apikey|token)'
            r'\s*=\s*["\'].*["\']'
        )

        for line_no, line in enumerate(lines, start=1):

            if re.search(pattern, line, re.IGNORECASE):

                self.findings.append(
                    {
                        "agent": "Security Agent",
                        "type": "Hardcoded Secret",
                        "severity": "HIGH",
                        "line": line_no,
                        "description":
                            "Hardcoded secret detected.",
                        "recommendation":
                            "Store secrets in environment variables or a secure vault."
                    }
                )

    # =====================================================
    # Weak Passwords
    # =====================================================

    def _detect_weak_passwords(self, source_code):

        lines = source_code.splitlines()

        pattern = (
            r'(password|passwd|pwd|secret)'
            r'\s*=\s*["\']([^"\']+)["\']'
        )

        weak_passwords = [
            "admin",
            "admin123",
            "password",
            "123456",
            "root",
            "test"
        ]

        for line_no, line in enumerate(lines, start=1):

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                value = match.group(2)

                if value.lower() in weak_passwords:

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Weak Authentication",
                            "severity": "HIGH",
                            "line": line_no,
                            "description":
                                f"Weak password '{value}' detected.",
                            "recommendation":
                                "Use a strong password and secure credential storage."
                        }
                    )

    # =====================================================
    # Unsafe eval()
    # =====================================================

    def _detect_eval_usage(self, source_code):

        lines = source_code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            if "eval(" in line:

                self.findings.append(
                    {
                        "agent": "Security Agent",
                        "type": "Unsafe eval()",
                        "severity": "HIGH",
                        "line": line_no,
                        "description":
                            "Use of eval() may allow arbitrary code execution.",
                        "recommendation":
                            "Avoid eval() or sanitize input."
                    }
                )
                    # =====================================================
    # Command Injection
    # =====================================================

    def _detect_command_injection(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"os\.system\s*\(",
            r"subprocess\.call\s*\(",
            r"subprocess\.run\s*\(",
            r"subprocess\.Popen\s*\(",
            r"Runtime\.getRuntime\(\)\.exec"
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Command Injection",
                            "severity": "CRITICAL",
                            "line": line_no,
                            "description":
                                "System command execution detected. User input may lead to command injection.",
                            "recommendation":
                                "Avoid direct command execution. Validate input and use secure APIs."
                        }
                    )

                    break

    # =====================================================
    # Weak Cryptography
    # =====================================================

    def _detect_weak_crypto(self, source_code):

        lines = source_code.splitlines()

        weak_algorithms = [
            "md5",
            "sha1",
            "des",
            "rc4"
        ]

        for line_no, line in enumerate(lines, start=1):

            for algo in weak_algorithms:

                if algo.lower() in line.lower():

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Weak Cryptography",
                            "severity": "HIGH",
                            "line": line_no,
                            "description":
                                f"Weak cryptographic algorithm '{algo.upper()}' detected.",
                            "recommendation":
                                "Use SHA-256, bcrypt, scrypt, or Argon2."
                        }
                    )

                    break

    # =====================================================
    # Cross Site Scripting (XSS)
    # =====================================================

    def _detect_xss(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"return\s+.*\+.*request",
            r"render_template_string",
            r"innerHTML\s*=",
            r"document\.write",
            r"<.*\+.*>"
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Cross Site Scripting (XSS)",
                            "severity": "HIGH",
                            "line": line_no,
                            "description":
                                "User input is directly inserted into HTML response.",
                            "recommendation":
                                "Escape user input and use secure template rendering."
                        }
                    )

                    break

        # =====================================================
    # Path Traversal
    # =====================================================

    def _detect_path_traversal(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"\.\./",
            r"os\.path\.join\(.*input",
            r"open\(.*input",
            r"open\(.*filename",
            r"File\(.*input"
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Path Traversal",
                            "severity": "HIGH",
                            "line": line_no,
                            "description":
                                "User-controlled file path may allow unauthorized file access.",
                            "recommendation":
                                "Validate file paths and restrict access to allowed directories."
                        }
                    )

                    break


    # =====================================================
    # Insecure Deserialization
    # =====================================================

    def _detect_insecure_deserialization(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"pickle\.loads\s*\(",
            r"pickle\.load\s*\(",
            r"yaml\.load\s*\(",
            r"ObjectInputStream",
            r"readObject\s*\("
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Insecure Deserialization",
                            "severity": "CRITICAL",
                            "line": line_no,
                            "description":
                                "Unsafe deserialization of untrusted data may allow remote code execution.",
                            "recommendation":
                                "Avoid deserializing untrusted data. Use safe serialization formats like JSON."
                        }
                    )

                    break


    # =====================================================
    # Weak Random Number Generation
    # =====================================================

    def _detect_weak_random(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"random\.random\s*\(",
            r"random\.randint\s*\(",
            r"random\.randrange\s*\(",
            r"random\.choice\s*\(",
            r"random\.choices\s*\(",
            r"Math\.random\s*\(",
            r"new\s+Random\s*\("
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Weak Random Number Generation",
                            "severity": "MEDIUM",
                            "line": line_no,
                            "description":
                                "Non-cryptographic random number generator detected.",
                            "recommendation":
                                "Use Python secrets module or Java SecureRandom for security-sensitive values."
                        }
                    )

                    break
                        # =====================================================
    # CSRF Detection
    # =====================================================

    def _detect_csrf(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"@PostMapping",
            r"@RequestMapping",
            r"csrf().disable",
            r"csrf=False",
            r"app\.post\("
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Possible CSRF",
                            "severity": "MEDIUM",
                            "line": line_no,
                            "description":
                                "POST endpoint detected. Verify CSRF protection is enabled.",
                            "recommendation":
                                "Enable CSRF protection or use anti-CSRF tokens."
                        }
                    )

                    break


    # =====================================================
    # SSRF Detection
    # =====================================================

    def _detect_ssrf(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"requests\.get\s*\(",
            r"requests\.post\s*\(",
            r"urllib\.request",
            r"URL\s*\(",
            r"HttpURLConnection"
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Possible SSRF",
                            "severity": "HIGH",
                            "line": line_no,
                            "description":
                                "Application performs outbound HTTP requests.",
                            "recommendation":
                                "Validate URLs and use allowlists for external requests."
                        }
                    )

                    break


    # =====================================================
    # XXE Detection
    # =====================================================

    def _detect_xxe(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"DocumentBuilderFactory",
            r"SAXParserFactory",
            r"XMLInputFactory",
            r"lxml",
            r"xml\.etree"
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Possible XXE",
                            "severity": "HIGH",
                            "line": line_no,
                            "description":
                                "XML parser detected. Ensure external entities are disabled.",
                            "recommendation":
                                "Disable DTDs and external entity processing."
                        }
                    )

                    break


    # =====================================================
    # Weak JWT Secret
    # =====================================================

    def _detect_weak_jwt(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"jwt",
            r"secret\s*=",
            r"HS256"
        ]

        for line_no, line in enumerate(lines, start=1):

            if re.search("|".join(patterns), line, re.IGNORECASE):

                self.findings.append(
                    {
                        "agent": "Security Agent",
                        "type": "Weak JWT Configuration",
                        "severity": "HIGH",
                        "line": line_no,
                        "description":
                            "JWT configuration detected. Verify strong secret and secure algorithm.",
                        "recommendation":
                            "Use a strong secret key and rotate it regularly."
                    }
                )


    # =====================================================
    # Debug Mode Enabled
    # =====================================================

    def _detect_debug_mode(self, source_code):

        lines = source_code.splitlines()

        patterns = [
            r"debug=True",
            r"setDebugEnabled",
            r"app\.run\(.*debug"
        ]

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line, re.IGNORECASE):

                    self.findings.append(
                        {
                            "agent": "Security Agent",
                            "type": "Debug Mode Enabled",
                            "severity": "LOW",
                            "line": line_no,
                            "description":
                                "Application is running in debug mode.",
                            "recommendation":
                                "Disable debug mode in production."
                        }
                    )

                    break