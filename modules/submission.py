import os
from datetime import datetime


class Submission:

    def __init__(self, filename, language, source_code):

        self.filename = filename
        self.language = language
        self.source_code = source_code
        self.upload_time = datetime.now()

    def get_details(self):

        return {
            "Filename": self.filename,
            "Language": self.language,
            "Upload Time": self.upload_time.strftime("%d-%m-%Y %H:%M:%S"),
            "Lines of Code": len(self.source_code.splitlines())
        }


def save_uploaded_file(uploaded_file):

    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def create_submission(uploaded_file=None, pasted_code="", language="Auto Detect"):

    if uploaded_file is not None:

        source_code = uploaded_file.getvalue().decode("utf-8")

        if language == "Auto Detect":

            if uploaded_file.name.endswith(".py"):
                language = "Python"

            elif uploaded_file.name.endswith(".java"):
                language = "Java"

        submission = Submission(
            uploaded_file.name,
            language,
            source_code
        )

        save_uploaded_file(uploaded_file)

        return submission

    elif pasted_code.strip() != "":

        submission = Submission(
            "Pasted Code",
            language,
            pasted_code
        )

        return submission

    return None