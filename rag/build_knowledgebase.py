import os

from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embedding import create_embeddings
from rag.vector_store import create_vector_store


def build_knowledge_base():
    try:
        os.makedirs("chroma_db", exist_ok=True)

        documents = load_documents("knowledge_base")

        if not documents:
            return "No PDF documents found in the knowledge_base folder."

        chunks = split_documents(documents)

        embeddings = create_embeddings()

        create_vector_store(chunks, embeddings)

        return "Knowledge Base Created Successfully!"

    except Exception as e:
        return f"Error: {str(e)}"