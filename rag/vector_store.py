import os

from langchain_community.vectorstores import Chroma


DB_PATH = "chroma_db"

os.makedirs(DB_PATH, exist_ok=True)


def create_vector_store(
    chunks,
    embedding_model
):

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )


def load_vector_store(
    embedding_model
):

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )