from radon.complexity import cc_visit


class RadonRunner:
    """
    Executes Radon to calculate Cyclomatic Complexity.
    No complexity rules are implemented manually.
    """

    def __init__(self):
        pass

    def run(self, code):

        findings = []

        try:

            results = cc_visit(code)

            for block in results:

                findings.append(
                    {
                        "agent": "Code Analysis Agent",
                        "tool": "Radon",
                        "name": block.name,
                        "type": block.__class__.__name__,
                        "complexity": block.complexity,
                        "rank": block.letter,
                        "line": block.lineno,
                        "end_line": block.endline,
                    }
                )

        except Exception as e:

            findings.append(
                {
                    "agent": "Code Analysis Agent",
                    "tool": "Radon",
                    "error": str(e)
                }
            )

        return findings