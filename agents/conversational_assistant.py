from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from rag.embedding import get_embedding_model
from rag.vector_store import load_vector_store
from rag.groq_model import get_groq_model


class ConversationalAssistant:
    """
    RAG-based Secure Coding Assistant.

    Flow:

    User Question
          |
          v
    Chroma Vector Search
          |
          v
    Relevant OWASP Documents
          |
          v
    Groq LLM
          |
          v
    Secure Coding Answer

    No hardcoded vulnerability knowledge.
    """

    def __init__(self):

        # -------------------------------
        # Embedding Model
        # -------------------------------

        self.embedding_model = get_embedding_model()


        # -------------------------------
        # Vector Database
        # -------------------------------

        self.vector_store = load_vector_store(
            self.embedding_model
        )


        # -------------------------------
        # Retriever
        # MMR improves RAG accuracy
        # -------------------------------

        self.retriever = self.vector_store.as_retriever(

            search_type="mmr",

            search_kwargs={
                "k": 3,
                "fetch_k": 10,
                "lambda_mult": 0.7
            }

        )


        # -------------------------------
        # LLM
        # -------------------------------

        self.llm = get_groq_model()



        # -------------------------------
        # RAG Prompt
        # -------------------------------

        prompt = ChatPromptTemplate.from_template(

"""
You are an AI Secure Coding Assistant.

Your job is to answer developer security questions
using ONLY the provided knowledge base context.

Rules:

1. Use only retrieved documents.
2. Do not use your own knowledge.
3. Do not guess.
4. If context does not contain the answer,
reply exactly:

"I could not find this information in the knowledge base."

5. Explain:
   - Vulnerability concept
   - Security impact
   - OWASP category if available
   - Prevention method
   - Secure coding example if available

Retrieved Context:

{context}


Developer Question:

{input}


Answer:

"""
        )


        # -------------------------------
        # Document Chain
        # -------------------------------

        document_chain = create_stuff_documents_chain(

            self.llm,

            prompt

        )


        # -------------------------------
        # Retrieval Chain
        # -------------------------------

        self.chain = create_retrieval_chain(

            self.retriever,

            document_chain

        )



    def ask(
        self,
        question: str
    ):


        result = self.chain.invoke(

            {
                "input": question
            }

        )


        answer = result.get(

            "answer",

            "No response generated."

        )


        sources = []


        # Retrieved documents

        documents = result.get(

            "context",

            []

        )


        for doc in documents:


            source = doc.metadata.get(

                "source",

                "Unknown"

            )


            if source not in sources:

                sources.append(source)



        return {

            "question": question,

            "answer": answer,

            "sources": sources

        }




    def retrieve_documents(

        self,

        query: str,

        k: int = 3

    ):

        """
        Used for debugging RAG retrieval.
        """

        return self.vector_store.similarity_search(

            query,

            k=k

        )





# =================================================
# Lazy Singleton
# =================================================

@lru_cache(maxsize=1)

def get_assistant():

    return ConversationalAssistant()



# =================================================
# UI Wrapper
# =================================================

def ask_question(question: str):

    assistant = get_assistant()

    return assistant.ask(question)