import os


UPLOAD_FOLDER = "uploads"


def create_upload_folder():

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def save_file(uploaded_file):

    create_upload_folder()

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def read_file(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except UnicodeDecodeError:
        return None


def delete_file(file_path):

    if os.path.exists(file_path):
        os.remove(file_path)