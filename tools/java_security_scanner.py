from tree_sitter import Parser, Language
import tree_sitter_java


class JavaSecurityScanner:
    """
    Java AST Analyzer.

    Uses Tree-sitter for Java parsing.
    No vulnerability rules.
    No regex detection.
    Security analysis is handled by AI/RAG agent.
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

            "type":
            node.type,

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



    def run(self, code):

        """
        Returns Java AST information.

        SecurityAgent + RAG + Groq
        will analyze vulnerabilities.
        """


        tree = self.parser.parse(

            bytes(
                code,
                "utf8"
            )

        )


        root = tree.root_node


        ast_data = self.extract_node(
            root,
            code
        )


        return ast_data