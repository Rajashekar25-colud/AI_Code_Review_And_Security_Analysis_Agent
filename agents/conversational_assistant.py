from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag.embedding import get_embedding_model
from rag.vector_store import load_vector_store
from rag.groq_model import get_groq_model


MAX_HISTORY_TURNS = 6
MAX_FINDINGS_IN_CONTEXT = 8


def format_chat_history(chat_history):
    """
    Turns [{"question": ..., "answer": ...}, ...] into a plain-text
    transcript the model can use for follow-up questions
    ("can you fix it?", "explain that more").
    """

    if not chat_history:
        return "No previous conversation."

    recent = chat_history[-MAX_HISTORY_TURNS:]

    lines = []

    for turn in recent:

        question = turn.get("question", "")
        answer = turn.get("answer", "")

        if question:
            lines.append(f"Developer: {question}")

        if answer:
            lines.append(f"Assistant: {answer}")

    return "\n".join(lines) if lines else "No previous conversation."


def format_review_findings(findings):
    """
    Summarizes the current review's findings (no line numbers) so
    follow-up questions can refer to "this scan" / "finding #2"
    without the model inventing details.
    """

    if not findings:
        return "No active code review findings for this conversation."

    lines = []

    for index, finding in enumerate(
        findings[:MAX_FINDINGS_IN_CONTEXT], start=1
    ):

        severity = str(finding.get("severity", "LOW")).upper()
        title = finding.get("type") or finding.get("category") or "Finding"
        description = finding.get("description", "")
        recommendation = finding.get("recommendation", "")

        entry = f"{index}. [{severity}] {title} - {description}"

        if recommendation:
            entry += f" (Suggested fix: {recommendation})"

        lines.append(entry)

    remaining = len(findings) - MAX_FINDINGS_IN_CONTEXT

    if remaining > 0:
        lines.append(f"...and {remaining} more finding(s).")

    return "\n".join(lines)


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
        # RAG + Follow-up Prompt
        #
        # In addition to the knowledge-base context, the model
        # receives the conversation so far and the findings of the
        # review currently being discussed, so it can answer
        # ChatGPT-style follow-ups ("fix that", "explain more")
        # that refer back to earlier turns or to this scan.
        # -------------------------------

        self.prompt = ChatPromptTemplate.from_template(

"""
You are an AI Secure Coding Assistant embedded in a code review
platform. You answer developer questions about secure coding and,
when relevant, about the findings from the developer's current
code review.

Rules:

1. Ground vulnerability/best-practice explanations in the
   retrieved knowledge base context below.
2. Use the "Current Code Review Findings" section only to answer
   questions about *this* scan (e.g. "explain finding 2",
   "how do I fix the hardcoded secret"). Do not invent findings
   that are not listed there.
3. Use "Conversation So Far" to resolve follow-up questions that
   refer to earlier turns (e.g. "can you fix it?", "explain that
   more"). Do not repeat the full previous answer verbatim.
4. Do not guess or fabricate facts. If the knowledge base context
   does not contain the answer and the question is not about the
   current review, reply exactly:
   "I could not find this information in the knowledge base."
5. Where relevant, explain: the vulnerability concept, security
   impact, OWASP category (if available), prevention method, and
   a secure coding example.
6. Never reference specific line numbers.

Knowledge Base Context:
{context}

Current Code Review Findings:
{review_context}

Conversation So Far:
{chat_history}

Developer Question:
{input}

Answer:
"""
        )

        self.chain = self.prompt | self.llm | StrOutputParser()


    def ask(
        self,
        question: str,
        chat_history: list | None = None,
        review_findings: list | None = None
    ):

        documents = self.retriever.invoke(question)

        context = "\n\n".join(
            doc.page_content for doc in documents
        ) or "No relevant knowledge base documents found."

        sources = []

        for doc in documents:

            source = doc.metadata.get("source", "Unknown")

            if source not in sources:
                sources.append(source)

        answer = self.chain.invoke(
            {
                "input": question,
                "context": context,
                "chat_history": format_chat_history(chat_history),
                "review_context": format_review_findings(
                    review_findings or []
                )
            }
        )

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

def ask_question(
    question: str,
    chat_history: list | None = None,
    review_findings: list | None = None
):

    assistant = get_assistant()

    return assistant.ask(
        question,
        chat_history=chat_history,
        review_findings=review_findings
    )