from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from rag.embedding import get_embedding_model
from rag.vector_store import load_vector_store
from rag.groq_model import get_groq_model


class ConversationalAssistant:
    """
    RAG-powered conversational assistant for secure coding.
    Compatible with LangChain 1.x
    """

    def __init__(self):

        # Load embedding model
        self.embedding_model = get_embedding_model()

        # Load vector database
        self.vector_store = load_vector_store(
            self.embedding_model
        )

        # Retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 4
            }
        )

        # LLM
        self.llm = get_groq_model()

        # Prompt
        prompt = ChatPromptTemplate.from_template(
            """
You are an AI Secure Coding Assistant.

Answer ONLY using the retrieved knowledge.

Rules:

- Use only the provided context.
- Never invent information.
- If the answer is unavailable, reply:
  "I could not find this information in the knowledge base."
- Explain security concepts clearly.
- Mention OWASP Secure Coding practices whenever applicable.

Context:
{context}

Question:
{input}

Answer:
"""
        )

        # Document Chain
        document_chain = create_stuff_documents_chain(
            self.llm,
            prompt
        )

        # Retrieval Chain
        self.chain = create_retrieval_chain(
            self.retriever,
            document_chain
        )

    # =====================================================
    # Ask Question
    # =====================================================

    def ask(self, question: str):

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

        for doc in result.get(
            "context",
            []
        ):

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

    # =====================================================
    # Retrieve Documents
    # =====================================================

    def retrieve_documents(
        self,
        query: str,
        k: int = 4
    ):

        return self.vector_store.similarity_search(
            query=query,
            k=k
        )


# =====================================================
# Global Assistant Instance
# =====================================================

assistant = ConversationalAssistant()


# =====================================================
# Helper Function
# =====================================================

def ask_question(question: str):
    """
    Wrapper function used by ui/assistant.py
    """

    return assistant.ask(question)