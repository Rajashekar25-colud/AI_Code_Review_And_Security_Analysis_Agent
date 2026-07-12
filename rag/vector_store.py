from langchain_chroma import Chroma
from langchain_core.documents import Document

DB_PATH = "chroma_db"


def create_vector_store(chunks, embedding_model):

    documents = []

    for chunk in chunks:
        documents.append(Document(page_content=chunk))

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    return vector_store


def load_vector_store(embedding_model):

    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )