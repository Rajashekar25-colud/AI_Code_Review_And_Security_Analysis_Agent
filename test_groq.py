from rag.groq_model import get_groq_model


llm = get_groq_model()


response = llm.invoke(
    "Explain SQL Injection in one sentence"
)


print(response.content)