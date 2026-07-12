import os


def detect_language(source):

    # -----------------------------
    # Check file extension
    # -----------------------------

    extension = os.path.splitext(source)[1].lower()


    if extension == ".py":
        return "Python"


    if extension == ".java":
        return "Java"



    # -----------------------------
    # Detect from pasted source code
    # -----------------------------

    code = source



    # Python indicators

    python_score = 0

    python_patterns = [
        "def ",
        "print(",
        "import ",
        "from ",
        "elif ",
        "self",
        "True",
        "False",
        "None",
        "input(",
        "range("
    ]


    for pattern in python_patterns:

        if pattern in code:

            python_score += 1



    # Java indicators

    java_score = 0

    java_patterns = [
        "public class",
        "class ",
        "public static void main",
        "System.out.println",
        "import java",
        "String[] args",
        "Scanner"
    ]


    for pattern in java_patterns:

        if pattern in code:

            java_score += 1



    # Result

    if python_score > java_score and python_score > 0:

        return "Python"


    elif java_score > python_score and java_score > 0:

        return "Java"


    else:

        return "Unknown"



def is_supported_file(filename):

    supported_extensions = [
        ".py",
        ".java"
    ]

    extension = os.path.splitext(filename)[1].lower()

    return extension in supported_extensions