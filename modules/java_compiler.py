import re
import shutil
import subprocess
import tempfile
from pathlib import Path


class JavaCompiler:
    """
    Dynamically compiles Java source code if javac is available.

    On platforms without a JDK (e.g. Streamlit Cloud),
    compilation is skipped gracefully instead of crashing.
    """

    PUBLIC_CLASS_PATTERN = re.compile(
        r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+([A-Za-z_]\w*)"
    )

    def __init__(self, javac_path=None):
        self.javac = javac_path or shutil.which("javac")
        self.available = self.javac is not None

    def is_available(self):
        """Returns True if javac is available."""
        return self.available

    def _extract_public_class_name(self, source_code: str) -> str:
        match = self.PUBLIC_CLASS_PATTERN.search(source_code)

        if not match:
            raise ValueError(
                "No public class found in the submitted Java source."
            )

        return match.group(1)

    def compile(self, source_code: str):
        """
        Compile Java source code.

        Returns:
            dict containing compilation status.
        """

        if not self.available:
            return {
                "status": "skipped",
                "success": False,
                "message": (
                    "Java compiler (javac) is not available on this system. "
                    "Compilation skipped."
                ),
                "class_dir": None,
            }

        class_name = self._extract_public_class_name(source_code)

        temp_dir = tempfile.mkdtemp(prefix="java_compile_")

        java_file = Path(temp_dir) / f"{class_name}.java"

        java_file.write_text(
            source_code,
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                self.javac,
                "-d",
                temp_dir,
                str(java_file),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "status": "failed",
                "success": False,
                "message": result.stderr,
                "class_dir": None,
            }

        return {
            "status": "success",
            "success": True,
            "message": "Compilation successful.",
            "class_dir": temp_dir,
        }