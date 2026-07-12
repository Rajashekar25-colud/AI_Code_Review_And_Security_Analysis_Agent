from rag.groq_model import get_groq_model

model = get_groq_model()

response = model.invoke("Explain SQL Injection in one sentence.")

print(response.content)