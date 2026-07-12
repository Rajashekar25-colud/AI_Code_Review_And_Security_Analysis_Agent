import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

DB_PATH = "chroma_db"

# Create database folder if it doesn't exist
os.makedirs(DB_PATH, exist_ok=True)


def create_vector_store(chunks, embedding_model):
    """
    Create and persist the Chroma vector database.
    """

    documents = [
        Document(page_content=chunk)
        for chunk in chunks
    ]

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=DB_PATH,
    )

    return vector_store


def load_vector_store(embedding_model):
    """
    Load an existing Chroma vector database.
    """

    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model,
    )

    return vector_store