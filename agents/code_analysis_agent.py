import re


class CodeAnalysisAgent:

    def __init__(self):
        pass

    # =====================================================
    # Main Analysis
    # =====================================================

    def analyze(self, code, language):

        findings = []

        findings.extend(self._detect_print_statements(code, language))
        findings.extend(self._detect_long_lines(code))
        findings.extend(self._detect_long_methods(code, language))
        findings.extend(self._detect_many_parameters(code, language))
        findings.extend(self._detect_magic_numbers(code))
        findings.extend(self._detect_todo_comments(code))
        findings.extend(self._detect_duplicate_imports(code))
        findings.extend(self._detect_unused_imports(code))
        findings.extend(self._detect_global_variables(code))
        findings.extend(self._detect_bare_except(code))
        findings.extend(self._detect_generic_exception(code))
        findings.extend(self._detect_empty_exception(code))
        findings.extend(self._detect_infinite_loop(code))
        findings.extend(self._detect_deep_nesting(code))

        return {
            "agent": "Code Analysis Agent",
            "findings": findings
        }

    # =====================================================
    # Console Output
    # =====================================================

    def _detect_print_statements(self, code, language):

        findings = []

        lines = code.splitlines()

        if language == "Python":
            keyword = "print("

        elif language == "Java":
            keyword = "System.out.println"

        else:
            return findings

        for line_no, line in enumerate(lines, start=1):

            if keyword in line:

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "type": "Console Output",
                        "severity": "LOW",
                        "line": line_no,
                        "description": "Console output detected.",
                        "recommendation": "Use a logging framework instead."
                    }
                )

        return findings

    # =====================================================
    # Long Lines
    # =====================================================

    def _detect_long_lines(self, code):

        findings = []

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            if len(line) > 120:

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "type": "Long Line",
                        "severity": "LOW",
                        "line": line_no,
                        "description": "Line exceeds 120 characters.",
                        "recommendation": "Break the line into multiple shorter lines."
                    }
                )

        return findings

    # =====================================================
    # Long Methods
    # =====================================================

    def _detect_long_methods(self, code, language):

        findings = []

        lines = code.splitlines()

        method_start = None
        method_name = ""
        brace_count = 0

        for i, line in enumerate(lines):

            # ---------------- Python ----------------

            if language == "Python":

                if re.match(r"\s*def\s+\w+", line):

                    if method_start is not None:

                        length = i - method_start

                        if length > 30:

                            findings.append(
                                {
                                    "agent": "Code Analysis Agent",
                                    "type": "Long Method",
                                    "severity": "MEDIUM",
                                    "line": method_start + 1,
                                    "description": f"{method_name} contains {length} lines.",
                                    "recommendation": "Split into smaller methods."
                                }
                            )

                    method_start = i
                    method_name = line.strip()

            # ---------------- Java ----------------

            elif language == "Java":

                if re.search(r"(public|private|protected).*?\(", line):

                    method_start = i
                    method_name = line.strip()
                    brace_count = line.count("{")

                if method_start is not None:

                    brace_count += line.count("{")
                    brace_count -= line.count("}")

                    if brace_count == 0:

                        length = i - method_start + 1

                        if length > 30:

                            findings.append(
                                {
                                    "agent": "Code Analysis Agent",
                                    "type": "Long Method",
                                    "severity": "MEDIUM",
                                    "line": method_start + 1,
                                    "description": f"{method_name} contains {length} lines.",
                                    "recommendation": "Split into smaller methods."
                                }
                            )

                        method_start = None

        # Handle last Python method

        if language == "Python" and method_start is not None:

            length = len(lines) - method_start

            if length > 30:

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "type": "Long Method",
                        "severity": "MEDIUM",
                        "line": method_start + 1,
                        "description": f"{method_name} contains {length} lines.",
                        "recommendation": "Split into smaller methods."
                    }
                )

        return findings
            # =====================================================
    # Too Many Parameters
    # =====================================================

    def _detect_many_parameters(self, code, language):

        findings = []

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            if "(" in line and ")" in line:

                match = re.search(r"\((.*?)\)", line)

                if match:

                    params = match.group(1).strip()

                    if not params:
                        continue

                    count = len(
                        [
                            p.strip()
                            for p in params.split(",")
                            if p.strip()
                        ]
                    )

                    if count > 5:

                        findings.append(
                            {
                                "agent": "Code Analysis Agent",
                                "type": "Too Many Parameters",
                                "severity": "MEDIUM",
                                "line": line_no,
                                "description": f"Method has {count} parameters.",
                                "recommendation": "Reduce parameter count by introducing an object."
                            }
                        )

        return findings

    # =====================================================
    # Magic Numbers
    # =====================================================

    def _detect_magic_numbers(self, code):

        findings = []

        ignore = {"0", "1", "2", "-1"}

        pattern = r"\b\d+\b"

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            stripped = line.strip()

            if stripped.startswith("#") or stripped.startswith("//"):
                continue

            numbers = re.findall(pattern, line)

            for number in numbers:

                if number not in ignore:

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Magic Number",
                            "severity": "LOW",
                            "line": line_no,
                            "description": f"Magic number '{number}' detected.",
                            "recommendation": "Replace it with a named constant."
                        }
                    )

        return findings

    # =====================================================
    # TODO / FIXME Comments
    # =====================================================

    def _detect_todo_comments(self, code):

        findings = []

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            upper = line.upper()

            if "TODO" in upper or "FIXME" in upper:

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "type": "TODO Comment",
                        "severity": "LOW",
                        "line": line_no,
                        "description": "Pending TODO/FIXME comment found.",
                        "recommendation": "Resolve or remove TODO/FIXME comments."
                    }
                )

        return findings

    # =====================================================
    # Duplicate Imports
    # =====================================================

    def _detect_duplicate_imports(self, code):

        findings = []

        seen = {}

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            text = line.strip()

            if text.startswith("import ") or text.startswith("from "):

                if text in seen:

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Duplicate Import",
                            "severity": "LOW",
                            "line": line_no,
                            "description": f"Duplicate import '{text}'.",
                            "recommendation": "Remove duplicate imports."
                        }
                    )

                else:

                    seen[text] = line_no

        return findings

    # =====================================================
    # Unused Imports
    # =====================================================

    def _detect_unused_imports(self, code):

        findings = []

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            text = line.strip()

            if text.startswith("import "):

                modules = text.replace("import", "").split(",")

                for module in modules:

                    module = module.strip().split(".")[-1]

                    if code.count(module) == 1:

                        findings.append(
                            {
                                "agent": "Code Analysis Agent",
                                "type": "Unused Import",
                                "severity": "LOW",
                                "line": line_no,
                                "description": f"'{module}' appears unused.",
                                "recommendation": "Remove unused imports."
                            }
                        )

        return findings

    # =====================================================
    # Global Variables
    # =====================================================

    def _detect_global_variables(self, code):

        findings = []

        inside_function = False

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            stripped = line.strip()

            if stripped.startswith("def "):

                inside_function = True

            elif stripped.startswith("class "):

                inside_function = False

            if (
                not inside_function
                and "=" in stripped
                and not stripped.startswith("#")
                and not stripped.startswith("import")
                and not stripped.startswith("from")
            ):

                variable = stripped.split("=")[0].strip()

                if variable.isidentifier():

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Global Variable",
                            "severity": "LOW",
                            "line": line_no,
                            "description": f"Global variable '{variable}' detected.",
                            "recommendation": "Avoid global variables where possible."
                        }
                    )

        return findings
            # =====================================================
    # Bare Except (Python)
    # =====================================================

    def _detect_bare_except(self, code):

        findings = []

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            if re.match(r"\s*except\s*:", line):

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "type": "Bare Except",
                        "severity": "HIGH",
                        "line": line_no,
                        "description": "Bare except catches all exceptions.",
                        "recommendation": "Catch specific exceptions instead."
                    }
                )

        return findings

    # =====================================================
    # Generic Exception Catch
    # =====================================================

    def _detect_generic_exception(self, code):

        findings = []

        patterns = [
            r"catch\s*\(\s*Exception",
            r"catch\s*\(\s*Throwable"
        ]

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line):

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Generic Exception Catch",
                            "severity": "MEDIUM",
                            "line": line_no,
                            "description": "Generic exception is being caught.",
                            "recommendation": "Catch specific exception types."
                        }
                    )

                    break

        return findings

    # =====================================================
    # Empty Exception Blocks
    # =====================================================

    def _detect_empty_exception(self, code):

        findings = []

        lines = code.splitlines()

        for i in range(len(lines) - 1):

            current = lines[i].strip()
            nxt = lines[i + 1].strip()

            if current.startswith("except"):

                if nxt == "" or nxt == "pass":

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Empty Exception Block",
                            "severity": "HIGH",
                            "line": i + 1,
                            "description": "Exception is silently ignored.",
                            "recommendation": "Log or handle the exception."
                        }
                    )

            if current.startswith("catch"):

                if nxt == "{":

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Empty Catch Block",
                            "severity": "HIGH",
                            "line": i + 1,
                            "description": "Empty catch block detected.",
                            "recommendation": "Handle or log the exception."
                        }
                    )

        return findings

    # =====================================================
    # Infinite Loop
    # =====================================================

    def _detect_infinite_loop(self, code):

        findings = []

        patterns = [
            r"while\s+True",
            r"while\s*\(\s*true\s*\)"
        ]

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            for pattern in patterns:

                if re.search(pattern, line):

                    findings.append(
                        {
                            "agent": "Code Analysis Agent",
                            "type": "Possible Infinite Loop",
                            "severity": "MEDIUM",
                            "line": line_no,
                            "description": "Potential infinite loop detected.",
                            "recommendation": "Ensure the loop has a termination condition."
                        }
                    )

                    break

        return findings

    # =====================================================
    # Deep Nesting
    # =====================================================

    def _detect_deep_nesting(self, code):

        findings = []

        lines = code.splitlines()

        for line_no, line in enumerate(lines, start=1):

            depth = (len(line) - len(line.lstrip())) // 4

            if depth >= 5:

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "type": "Deep Nesting",
                        "severity": "MEDIUM",
                        "line": line_no,
                        "description": f"Nesting depth is {depth}.",
                        "recommendation": "Refactor nested logic into smaller methods."
                    }
                )

        return findings