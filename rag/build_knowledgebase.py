import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def load_documents():

    docs = []

    folder = "knowledge_base"

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            loader = PyPDFLoader(path)

            documents = loader.load()

            docs.extend(documents)

            print(f"Loaded: {file}")

    return docs


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(documents)


def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )


# 👇 ADD THIS FUNCTION
def build_knowledge_base():

    documents = load_documents()

    chunks = split_documents(documents)

    create_vector_store(chunks)

    return "Knowledge Base built successfully!"


if __name__ == "__main__":

    build_knowledge_base()