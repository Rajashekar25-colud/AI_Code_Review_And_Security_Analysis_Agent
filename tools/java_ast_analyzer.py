from tree_sitter import Parser, Language
import tree_sitter_java


class JavaASTAnalyzer:
    """
    Java AST Analyzer.

    Uses Tree-sitter for parsing Java source code.
    Does not contain vulnerability rules.
    """


    def __init__(self):

        self.parser = Parser()

        java = Language(
            tree_sitter_java.language()
        )

        # tree-sitter 0.26+
        self.parser.language = java



    def get_text(self, node, code):

        return code[
            node.start_byte:
            node.end_byte
        ]



    def extract_node(self, node, code):

        data = {

            "type": node.type,

            "text":
            self.get_text(
                node,
                code
            ),

            "line":
            node.start_point[0] + 1

        }

        children = []

        for child in node.children:

            children.append(
                self.extract_node(
                    child,
                    code
                )
            )


        if children:

            data["children"] = children


        return data



    def analyze(self, code):

        tree = self.parser.parse(
            bytes(
                code,
                "utf8"
            )
        )


        root = tree.root_node


        return self.extract_node(
            root,
            code
        )