import ast


class CodeAnalysisAgent:

    def __init__(self):
        self.findings = []

    def analyze(self, source_code, language):

        self.findings = []

        if language == "Python":
            self._analyze_python(source_code)

        elif language == "Java":
            self._analyze_java(source_code)

        return self.findings

    # -----------------------------------
    # Python Analysis
    # -----------------------------------

    def _analyze_python(self, source_code):

        try:
            tree = ast.parse(source_code)

            self._check_long_methods(tree)

            self._check_poor_variable_names(tree)

            self._check_magic_numbers(tree)

        except Exception as e:

            self.findings.append(
                {
                    "agent": "Code Analysis",
                    "type": "Parsing Error",
                    "severity": "High",
                    "line": 0,
                    "description": str(e),
                    "recommendation": "Fix syntax before analysis."
                }
            )

    # -----------------------------------
    # Java Analysis (Placeholder)
    # -----------------------------------

    def _analyze_java(self, source_code):

        lines = source_code.splitlines()

        if len(lines) > 200:

            self.findings.append(
                {
                    "agent": "Code Analysis",
                    "type": "Large Java File",
                    "severity": "Medium",
                    "line": 1,
                    "description": "Java source file is very large.",
                    "recommendation": "Split into smaller classes."
                }
            )

    # -----------------------------------
    # Long Method Detection
    # -----------------------------------

    def _check_long_methods(self, tree):

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                total_lines = len(node.body)

                if total_lines > 30:

                    self.findings.append(
                        {
                            "agent": "Code Analysis",
                            "type": "Long Method",
                            "severity": "Medium",
                            "line": node.lineno,
                            "description": f"Function '{node.name}' contains {total_lines} statements.",
                            "recommendation": "Split the function into smaller reusable functions."
                        }
                    )

    # -----------------------------------
    # Poor Naming Detection
    # -----------------------------------

    def _check_poor_variable_names(self, tree):

        bad_names = {
            "x",
            "y",
            "z",
            "a",
            "b",
            "c",
            "temp",
            "data",
            "obj"
        }

        for node in ast.walk(tree):

            if isinstance(node, ast.Name):

                if node.id in bad_names:

                    self.findings.append(
                        {
                            "agent": "Code Analysis",
                            "type": "Poor Variable Name",
                            "severity": "Low",
                            "line": node.lineno,
                            "description": f"Variable '{node.id}' is not descriptive.",
                            "recommendation": "Use meaningful variable names."
                        }
                    )

    # -----------------------------------
    # Magic Number Detection
    # -----------------------------------

    def _check_magic_numbers(self, tree):

        ignored = {0, 1, -1}

        for node in ast.walk(tree):

            if isinstance(node, ast.Constant):

                if isinstance(node.value, int):

                    if node.value not in ignored:

                        self.findings.append(
                            {
                                "agent": "Code Analysis",
                                "type": "Magic Number",
                                "severity": "Low",
                                "line": node.lineno,
                                "description": f"Magic number '{node.value}' found.",
                                "recommendation": "Replace with a named constant."
                            }
                        )