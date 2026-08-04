import re


class JavaQualityAnalyzer:
    """
    Custom Java code quality analyzer.

    Detects:
    - Unused local variables
    - Empty catch blocks
    - Simple code quality issues
    """

    def analyze(self, code):

        findings = []

        findings.extend(
            self.detect_unused_variables(code)
        )

        findings.extend(
            self.detect_empty_catch(code)
        )

        return findings


    def detect_unused_variables(self, code):

        findings = []

        variables = re.findall(
            r'\b(int|String|double|float|boolean|char)\s+(\w+)\s*=',
            code
        )


        for datatype, variable in variables:

            count = code.count(variable)

            if count == 1:

                findings.append(
                    {
                        "issue": "Unused Local Variable",
                        "severity": "MEDIUM",
                        "description":
                        f"Variable '{variable}' is declared but never used.",
                        "recommendation":
                        "Remove unused variables to improve readability and maintainability."
                    }
                )

        return findings



    def detect_empty_catch(self, code):

        findings = []

        pattern = r'catch\s*\([^)]*\)\s*\{\s*\}'

        matches = re.findall(
            pattern,
            code
        )


        if matches:

            findings.append(
                {
                    "issue": "Empty Catch Block",
                    "severity": "MEDIUM",
                    "description":
                    "Exception is caught but not handled.",
                    "recommendation":
                    "Handle exceptions properly or log the error."
                }
            )


        return findings