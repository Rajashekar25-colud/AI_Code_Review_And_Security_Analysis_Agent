import os
from langchain_huggingface import HuggingFaceEmbeddings


def create_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings



def generate_vectors(chunks):

    embeddings = create_embeddings()

    vectors = []


    for chunk in chunks:

        vector = embeddings.embed_query(chunk)

        vectors.append(
            {
                "text": chunk,
                "embedding": vector
            }
        )


    return vectors