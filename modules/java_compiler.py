import os
import subprocess
import tempfile


class JavaCompiler:
    """
    Compiles Java source code before SpotBugs analysis.
    """


    def compile(self, code):

        temp_dir = tempfile.mkdtemp()


        java_file = os.path.join(
            temp_dir,
            "Main.java"
        )


        with open(java_file, "w") as file:
            file.write(code)



        result = subprocess.run(
            [
                "javac",
                java_file
            ],
            capture_output=True,
            text=True
        )


        if result.returncode != 0:

            print(
                "Java Compilation Error:",
                result.stderr
            )

            return None



        return temp_dir