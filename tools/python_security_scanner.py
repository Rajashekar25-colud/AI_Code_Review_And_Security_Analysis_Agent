import ast
import json
import os


class SecurityRuleEngine(ast.NodeVisitor):

    def __init__(self, rule_file):

        self.findings = []

        self.rules = self.load_rules(rule_file)

        self.imports = {}



    # ==============================
    # Load Rules
    # ==============================

    def load_rules(self, rule_file):

        try:

            with open(
                rule_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                return data.get(
                    "rules",
                    []
                )


        except Exception:

            return []



    # ==============================
    # Import Tracking
    # ==============================

    def visit_Import(self, node):

        for item in node.names:

            self.imports[
                item.asname or item.name
            ] = item.name


        self.generic_visit(node)



    def visit_ImportFrom(self, node):

        for item in node.names:

            self.imports[
                item.asname or item.name
            ] = (
                node.module
                +
                "."
                +
                item.name
            )


        self.generic_visit(node)



    # ==============================
    # Function Call Detection
    # ==============================

    def visit_Call(self, node):

        function_name = self.extract_function_name(
            node
        )


        for rule in self.rules:


            if self.check_sink(
                rule,
                function_name
            ):

                self.add_finding(
                    rule,
                    node
                )


        self.generic_visit(node)



    # ==============================
    # Assignment Detection
    # ==============================

    def visit_Assign(self,node):

        variables=[]


        for target in node.targets:


            if isinstance(
                target,
                ast.Name
            ):

                variables.append(
                    target.id.lower()
                )


        value = self.extract_value(
            node.value
        )


        for rule in self.rules:


            if self.check_secret(
                rule,
                variables,
                value
            ):

                self.add_finding(
                    rule,
                    node
                )


        self.generic_visit(node)



    # ==============================
    # Function Name Extraction
    # ==============================

    def extract_function_name(self,node):


        if isinstance(
            node.func,
            ast.Name
        ):

            return node.func.id.lower()



        if isinstance(
            node.func,
            ast.Attribute
        ):


            parts=[]

            current=node.func


            while isinstance(
                current,
                ast.Attribute
            ):

                parts.append(
                    current.attr
                )

                current=current.value



            if isinstance(
                current,
                ast.Name
            ):

                parts.append(
                    current.id
                )


            return ".".join(
                reversed(parts)
            ).lower()



        return ""



    # ==============================
    # Extract Values
    # ==============================

    def extract_value(self,node):


        if isinstance(
            node,
            ast.Constant
        ):

            return str(
                node.value
            ).lower()



        if isinstance(
            node,
            ast.JoinedStr
        ):

            return "fstring"



        if isinstance(
            node,
            ast.BinOp
        ):

            return "concat"



        if isinstance(
            node,
            ast.Dict
        ):

            return "dict"



        if isinstance(
            node,
            ast.List
        ):

            return "list"



        return ""



    # ==============================
    # Sink Matching
    # ==============================

    def check_sink(
        self,
        rule,
        function_name
    ):


        patterns = rule.get(
            "patterns",
            {}
        )


        sinks = patterns.get(
            "sink",
            []
        )


        for sink in sinks:


            sink=sink.lower()



            if (
                function_name == sink
                or
                function_name.endswith(
                    "." + sink
                )
            ):

                return True



        return False



    # ==============================
    # Secret Detection
    # ==============================

    def check_secret(
        self,
        rule,
        variables,
        value
    ):


        patterns = rule.get(
            "patterns",
            {}
        )


        names = patterns.get(
            "variables",
            []
        )


        values = patterns.get(
            "values",
            []
        )



        for variable in variables:


            for name in names:


                if name.lower() in variable.lower():

                    return True




        for item in values:


            if item.lower() in value.lower():

                return True



        return False



    # ==============================
    # Add Finding
    # ==============================

    def add_finding(
        self,
        rule,
        node
    ):


        finding={


            "issue":
            rule.get(
                "name",
                "Security Issue"
            ),


            "rule_id":
            rule.get(
                "id"
            ),


            "category":
            rule.get(
                "category"
            ),


            "severity":
            rule.get(
                "severity",
                "MEDIUM"
            ),


            "line":
            getattr(
                node,
                "lineno",
                0
            ),


            "column":
            getattr(
                node,
                "col_offset",
                0
            ),


            "description":
            rule.get(
                "description",
                ""
            ),


            "recommendation":
            rule.get(
                "recommendation",
                ""
            )

        }



        key = (

            finding["rule_id"],

            finding["line"]

        )


        existing_keys = [

            (
                item["rule_id"],
                item["line"]
            )

            for item in self.findings

        ]



        if key not in existing_keys:

            self.findings.append(
                finding
            )





# ==================================
# Agent Entry Point
# ==================================

def scan_python_security(code):


    try:


        tree = ast.parse(
            code
        )


        rule_file = os.path.join(

            os.path.dirname(__file__),

            "python_security_rules.json"

        )


        scanner = SecurityRuleEngine(
            rule_file
        )


        scanner.visit(tree)



        return scanner.findings



    except SyntaxError as error:


        return [

            {

                "issue":
                "Syntax Error",


                "severity":
                "INFO",


                "line":
                error.lineno,


                "description":
                str(error),


                "recommendation":
                "Fix syntax errors before security scanning."

            }

        ]