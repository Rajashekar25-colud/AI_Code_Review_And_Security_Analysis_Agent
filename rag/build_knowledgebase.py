from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embedding import get_embedding_model
from rag.vector_store import create_vector_store


def build_knowledge_base():

    print("Loading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} pages.")

    print("Splitting documents...")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")

    embedding_model = get_embedding_model()

    print("Creating vector database...")

    create_vector_store(
        chunks,
        embedding_model
    )

    return "Knowledge Base built successfully!"


if __name__ == "__main__":

    print(build_knowledge_base())