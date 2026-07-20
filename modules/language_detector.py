import re


def detect_language(code, filename=None):
    """
    Detect programming language from filename or source code.
    Supports Python and Java.
    """

    # ----------------------------------------
    # 1. Detect by filename
    # ----------------------------------------
    if filename:
        filename = filename.lower().strip()

        if filename.endswith(".py"):
            return "Python"

        if filename.endswith(".java"):
            return "Java"

    # ----------------------------------------
    # 2. Empty code
    # ----------------------------------------
    if not code or not code.strip():
        return "Unknown"

    code_lower = code.lower()

    # ----------------------------------------
    # 3. Java patterns
    # ----------------------------------------
    java_patterns = [

        r"import\s+java",

        r"public\s+class",

        r"class\s+\w+",

        r"public\s+static\s+void\s+main",

        r"system\.out\.println",

        r"drivermanager",

        r"\bconnection\b",

        r"\bpreparedstatement\b",

        r"\bstatement\b",

        r"\bresultset\b",

        r"\bthrows\b",

        r"\bextends\b",

        r"\bimplements\b",

        r"\bstring\b",

        r"new\s+\w+",

        r"package\s+\w+",

        r"jdbc:",

        r"scanner\s+\w+",

        r"arraylist",

        r"hashmap"

    ]

    # ----------------------------------------
    # 4. Python patterns
    # ----------------------------------------
    python_patterns = [

        r"\bdef\b",

        r"\bfrom\b",

        r"\bimport\s+\w+",

        r"print\s*\(",

        r"self",

        r"__name__",

        r"async\s+def",

        r"lambda",

        r"try:",

        r"except",

        r"finally:",

        r"with\s+",

        r"yield",

        r"pass",

        r"none",

        r"true",

        r"false",

        r"pickle",

        r"os\.",

        r"subprocess",

        r"flask",

        r"django",

        r"streamlit",

        r"request\.",

        r"input\s*\(",

        r"open\s*\(",

        r"random\.",

        r"hashlib",

        r"eval\s*\("

    ]

    # ----------------------------------------
    # 5. Calculate score
    # ----------------------------------------
    java_score = 0
    python_score = 0

    for pattern in java_patterns:

        if re.search(pattern, code_lower):
            java_score += 1

    for pattern in python_patterns:

        if re.search(pattern, code_lower):
            python_score += 1

    # ----------------------------------------
    # 6. Decide language
    # ----------------------------------------
    if java_score > python_score:
        return "Java"

    if python_score > java_score:
        return "Python"

    # ----------------------------------------
    # 7. Extra fallback checks
    # ----------------------------------------

    # Java style
    if ";" in code and ("{" in code or "}" in code):
        return "Java"

    # Java database snippet
    if "drivermanager" in code_lower:
        return "Java"

    if "connection" in code_lower:
        return "Java"

    # Python indentation
    if ":" in code and (
        "def " in code_lower
        or "if " in code_lower
        or "for " in code_lower
        or "while " in code_lower
    ):
        return "Python"

    # Generic imports
    if re.search(r"import\s+java", code_lower):
        return "Java"

    if re.search(r"import\s+\w+", code_lower):
        return "Python"

    return "Unknown"