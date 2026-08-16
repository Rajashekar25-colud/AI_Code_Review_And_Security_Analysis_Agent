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

        detail = _describe_java_error(e)

        return False, f"Java Syntax Error: {detail}"


def _describe_java_error(error):
    """
    javalang's exceptions (JavaSyntaxError, LexerError, etc.) often
    have an empty str(error) - the useful diagnostic info instead
    lives on other attributes depending on the exception type. This
    pulls out whatever is actually available instead of showing a
    blank message.
    """

    text = str(error).strip()

    if text:
        return text

    # JavaSyntaxError commonly exposes .description and/or .at
    # (a token, which has a .position of (line, column)).
    parts = []

    description = getattr(error, "description", None)

    if description:
        parts.append(str(description))

    token = getattr(error, "at", None)

    if token is not None:

        position = getattr(token, "position", None)

        if position:
            parts.append(f"at line {position[0]}, column {position[1]}")

        token_value = getattr(token, "value", None)

        if token_value:
            parts.append(f"near '{token_value}'")

    if parts:
        return " ".join(parts)

    # Last resort: at least name the exception type so the person
    # isn't looking at a completely blank message.
    return (
        f"{type(error).__name__} "
        "(no further detail available from the parser - the code "
        "may use a Java syntax feature this parser doesn't support, "
        "or may genuinely contain an error)."
    )


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