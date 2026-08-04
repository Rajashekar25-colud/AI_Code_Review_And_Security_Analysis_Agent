import re
import shutil
import subprocess
import tempfile
from pathlib import Path


class JavaCompiler:
    """
    Compiles Java source code dynamically.

    Features:
    - Detects the public class name automatically.
    - Uses a temporary working directory.
    - Returns the compiled class directory.
    - No hardcoded filenames or paths.
    """

    PUBLIC_CLASS_PATTERN = re.compile(
        r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+([A-Za-z_]\w*)"
    )

    def __init__(self, javac_path=None):
        self.javac = javac_path or shutil.which("javac")

        if not self.javac:
            raise RuntimeError(
                "javac was not found. "
                "Install the JDK or set the JAVAC_PATH environment variable."
            )

    def _extract_public_class_name(self, source_code: str) -> str:
        match = self.PUBLIC_CLASS_PATTERN.search(source_code)

        if not match:
            raise ValueError(
                "No public class found in the submitted Java source."
            )

        return match.group(1)

    def compile(self, source_code: str):
        """
        Compiles Java source code.

        Returns:
            str: directory containing compiled .class files
        """

        class_name = self._extract_public_class_name(source_code)

        temp_dir = tempfile.mkdtemp(prefix="java_compile_")

        java_file = Path(temp_dir) / f"{class_name}.java"

        java_file.write_text(
            source_code,
            encoding="utf-8"
        )

        result = subprocess.run(
            [
                self.javac,
                "-d",
                temp_dir,
                str(java_file)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Java compilation failed:\n{result.stderr}"
            )

        return temp_dir