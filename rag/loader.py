import os

from langchain_community.document_loaders import PyPDFLoader


KNOWLEDGE_BASE_FOLDER = "knowledge_base"


def load_documents():

    documents = []

    if not os.path.exists(KNOWLEDGE_BASE_FOLDER):
        raise FileNotFoundError(
            f"{KNOWLEDGE_BASE_FOLDER} folder not found."
        )

    for file in os.listdir(KNOWLEDGE_BASE_FOLDER):

        if file.lower().endswith(".pdf"):

            path = os.path.join(
                KNOWLEDGE_BASE_FOLDER,
                file
            )

            loader = PyPDFLoader(path)

            documents.extend(loader.load())

            print(f"Loaded: {file}")

    return documents