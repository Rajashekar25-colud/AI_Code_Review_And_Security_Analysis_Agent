import ast


class PythonSecurityScanner(ast.NodeVisitor):

    def __init__(self):

        self.findings = []

        self.has_csrf = False


    def visit_Call(self,node):

        source = ast.unparse(node)


        # Detect CSRF protection

        if (
            "CSRFProtect" in source
            or "csrf_token" in source
            or "validate_csrf" in source
        ):

            self.has_csrf = True


        self.generic_visit(node)



    def visit_FunctionDef(self,node):

        function_code = ast.unparse(node)


        # Detect Flask POST routes

        if (
            "@app.route" in function_code
            and "POST" in function_code
            and "request.form" in function_code
        ):

            if not self.has_csrf:

                self.findings.append({

                    "issue":
                    "Cross Site Request Forgery (CSRF)",


                    "severity":
                    "HIGH",


                    "line":
                    node.lineno,


                    "description":
                    "POST endpoint accepts state-changing requests without CSRF protection.",


                    "recommendation":
                    "Enable Flask CSRF protection using Flask-WTF CSRFProtect and validate CSRF tokens."

                })


        self.generic_visit(node)



def scan_python_security(code):

    tree = ast.parse(code)

    scanner = PythonSecurityScanner()

    scanner.visit(tree)

    return scanner.findings