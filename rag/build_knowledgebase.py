import os
from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embedding import create_embeddings
from rag.vector_store import create_vector_store


def build_knowledge_base():

    print("Loading documents...")
    documents = load_documents("knowledge_base")

    print("Splitting documents...")
    chunks = split_documents(documents)

    print("Creating embeddings...")
    embeddings = create_embeddings()

    print("Creating vector database...")
    create_vector_store(chunks, embeddings)

    return "Knowledge Base Created Successfully!"