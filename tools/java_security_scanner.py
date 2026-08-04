from tree_sitter import Parser, Language
import tree_sitter_java


class JavaSecurityScanner:
    """
    Java AST Analyzer.

    Uses Tree-sitter for parsing Java source code.

    No vulnerability rules.
    No regex.
    No hardcoded security detection.

    Only extracts AST for downstream AI/RAG analysis.
    """

    def __init__(self):

        self.parser = Parser()

        java = Language(
            tree_sitter_java.language()
        )

        # tree-sitter >=0.25
        self.parser.language = java

    def get_text(
        self,
        node,
        source_bytes
    ):

        return source_bytes[
            node.start_byte:
            node.end_byte
        ].decode(
            "utf-8",
            errors="replace"
        )

    def extract_node(
        self,
        root,
        source_bytes
    ):

        root_data = {

            "type": root.type,

            "text": self.get_text(
                root,
                source_bytes
            ),

            "line": root.start_point[0] + 1
        }

        stack = [
            (
                root,
                root_data
            )
        ]

        while stack:

            node, node_dict = stack.pop()

            children = []

            for child in node.children:

                child_dict = {

                    "type": child.type,

                    "text": self.get_text(
                        child,
                        source_bytes
                    ),

                    "line": child.start_point[0] + 1
                }

                children.append(
                    child_dict
                )

                stack.append(
                    (
                        child,
                        child_dict
                    )
                )

            if children:

                node_dict["children"] = children

        return root_data

    def run(
        self,
        code
    ):
        """
        Parses Java source and returns AST information.

        Security detection is intentionally delegated to
        the LLM/RAG pipeline.
        """

        source_bytes = code.encode(
            "utf-8"
        )

        tree = self.parser.parse(
            source_bytes
        )

        ast_data = self.extract_node(
            tree.root_node,
            source_bytes
        )

        return [
            {
                "agent":
                "Java AST Analyzer",

                "tool":
                "Tree-sitter",

                "type":
                "Java AST",

                "severity":
                "INFO",

                "line":
                1,

                "description":
                "Java AST generated successfully.",

                "recommendation":
                "Use the AST as input for AI/RAG security analysis.",

                "ast":
                ast_data
            }
        ]