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
    # 2. Empty source
    # ----------------------------------------
    if not code or not code.strip():
        return "Unknown"

    code_lower = code.lower()

    # ----------------------------------------
    # 3. Java Patterns
    # ----------------------------------------
    java_patterns = [

        r"import\s+java",
        r"package\s+\w+",
        r"public\s+class",
        r"class\s+\w+",
        r"public\s+static\s+void\s+main",
        r"system\.out\.println",
        r"out\.println",
        r"request\.getparameter",
        r"response",
        r"httpservlet",
        r"servlet",
        r"getparameter",
        r"\bstring\b",
        r"\bint\b",
        r"\bdouble\b",
        r"\bboolean\b",
        r"\bvoid\b",
        r"\bextends\b",
        r"\bimplements\b",
        r"\bthrows\b",
        r"\bthrow\b",
        r"new\s+\w+",
        r"scanner",
        r"arraylist",
        r"linkedlist",
        r"hashmap",
        r"hashset",
        r"treemap",
        r"drivermanager",
        r"\bconnection\b",
        r"\bpreparedstatement\b",
        r"\bstatement\b",
        r"\bresultset\b",
        r"jdbc:",
        r"catch\s*\(",
        r"finally",
        r"try\s*\{",
        r"private\s+",
        r"protected\s+",
        r"public\s+",
        r"final\s+",
        r"static\s+",
        r"this\.",
        r"super\.",
        r"@override",
        r"@restcontroller",
        r"@requestmapping",
        r"@getmapping",
        r"@postmapping",
        r"@service",
        r"@repository",
        r"@entity",
    ]

    # ----------------------------------------
    # 4. Python Patterns
    # ----------------------------------------
    python_patterns = [

        r"\bdef\b",
        r"\bfrom\b",
        r"\bimport\s+\w+",
        r"print\s*\(",
        r"self",
        r"__name__",
        r"async\s+def",
        r"await",
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
        r"os\.",
        r"subprocess",
        r"pickle",
        r"hashlib",
        r"django",
        r"flask",
        r"streamlit",
        r"fastapi",
        r"input\s*\(",
        r"open\s*\(",
        r"eval\s*\(",
        r"exec\s*\(",
        r"random\.",
        r"numpy",
        r"pandas",
        r"matplotlib",
        r"plt\.",
        r"if __name__",
        r"class\s+\w+\(",
    ]

    # ----------------------------------------
    # 5. Score Matching
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
    # 6. Decide by score
    # ----------------------------------------
    if java_score > python_score and java_score > 0:
        return "Java"

    if python_score > java_score and python_score > 0:
        return "Python"

    # ----------------------------------------
    # 7. Java Fallbacks
    # ----------------------------------------

    if ";" in code and ("{" in code or "}" in code):
        return "Java"

    if "system.out.println" in code_lower:
        return "Java"

    if "out.println" in code_lower:
        return "Java"

    if "getparameter" in code_lower:
        return "Java"

    if "request." in code_lower:
        return "Java"

    if "response." in code_lower:
        return "Java"

    if "drivermanager" in code_lower:
        return "Java"

    if "preparedstatement" in code_lower:
        return "Java"

    if "connection" in code_lower:
        return "Java"

    if "resultset" in code_lower:
        return "Java"

    if "scanner" in code_lower:
        return "Java"

    if "arraylist" in code_lower:
        return "Java"

    if "hashmap" in code_lower:
        return "Java"

    if "string " in code_lower and ";" in code:
        return "Java"

    if "public " in code_lower:
        return "Java"

    if "private " in code_lower:
        return "Java"

    if "protected " in code_lower:
        return "Java"

    # ----------------------------------------
    # 8. Python Fallbacks
    # ----------------------------------------

    if ":" in code and (
        "def " in code_lower
        or "if " in code_lower
        or "for " in code_lower
        or "while " in code_lower
        or "with " in code_lower
    ):
        return "Python"

    if re.search(r"import\s+\w+", code_lower):
        return "Python"

    if "print(" in code_lower:
        return "Python"

    if "input(" in code_lower:
        return "Python"

    if "open(" in code_lower:
        return "Python"

    if "os." in code_lower:
        return "Python"

    # ----------------------------------------
    # 9. Unknown
    # ----------------------------------------
    return "Unknown"