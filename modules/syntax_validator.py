import ast
import javalang


def validate_python(code):
    """
    Check Python syntax.
    Returns (True, message) if valid,
    otherwise (False, error message).
    """

    try:
        ast.parse(code)
        return True, "Python syntax is valid."

    except SyntaxError as e:
        return False, f"Python Syntax Error: {e}"


def validate_java(code):
    """
    Check Java syntax.
    Returns (True, message) if valid,
    otherwise (False, error message).
    """

    try:
        javalang.parse.parse(code)
        return True, "Java syntax is valid."

    except Exception as e:
        return False, f"Java Syntax Error: {e}"


def validate_code(code, language):
    """
    Validate code based on selected language.
    """

    if language == "Python":
        return validate_python(code)

    elif language == "Java":
        return validate_java(code)

    else:
        return False, "Unsupported language."