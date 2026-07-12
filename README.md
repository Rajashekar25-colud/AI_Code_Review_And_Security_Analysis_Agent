# 🤖 AI Code Review & Security Analysis Agent

An AI-powered Code Review & Security Analysis platform that automatically analyzes Python and Java source code for syntax validation and builds a Retrieval-Augmented Generation (RAG) knowledge base from secure coding documents.

---

# 📌 Project Overview

Modern software development requires high-quality, secure, and maintainable code. Manual code reviews are often time-consuming and may overlook security vulnerabilities and coding best practices.

The AI Code Review & Security Analysis Agent is designed to simplify the initial stages of code review by allowing developers to submit source code, validate its syntax, and build a searchable secure coding knowledge base using Retrieval-Augmented Generation (RAG).

---

# ✨ Features

- Upload Python and Java source files
- Paste source code directly
- Automatic programming language detection
- Python syntax validation
- Java syntax validation
- Secure Coding Knowledge Base creation
- PDF document loading
- Document chunking
- HuggingFace embedding generation
- ChromaDB vector database indexing
- Streamlit-based interactive interface

---

# 🛠️ Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### AI & RAG

- LangChain
- HuggingFace Embeddings
- ChromaDB

### Document Processing

- PyPDF

### Programming Languages Supported

- Python
- Java

---

# 📂 Project Structure

```text
AI-Code-Review-Agent/
│
├── app.py
├── requirements.txt
├── .env
│
├── knowledge_base/
│   ├── OWASP_Top10.pdf
│   ├── Java_Secure_Coding.pdf
│   └── Secure_Coding_Guide.pdf
│
├── modules/
│   ├── file_handler.py
│   ├── language_detector.py
│   ├── submission.py
│   └── syntax_validator.py
│
├── rag/
│   ├── loader.py
│   ├── splitter.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── build_knowledgebase.py
│   └── groq_model.py
│
├── chroma_db/
│
└── uploads/
```

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/AI-Code-Review-Agent.git
```

### Navigate to the project

```bash
cd AI-Code-Review-Agent
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DB=chroma_db

KNOWLEDGE_BASE=knowledge_base

UPLOAD_FOLDER=uploads
```

### Run the application

```bash
streamlit run app.py
```

---

# 📚 Knowledge Base

The application builds a searchable vector database from secure coding documents such as:

- OWASP Top 10
- Java Secure Coding Guide
- Python Secure Coding Guide
- Secure Coding Best Practices

---

# 🔄 RAG Pipeline

```text
PDF Documents
      │
      ▼
Document Loader
      │
      ▼
Text Splitter
      │
      ▼
HuggingFace Embeddings
      │
      ▼
ChromaDB Vector Store
```

---

# 🧪 Functionalities

### Code Submission

- Upload Python files (.py)
- Upload Java files (.java)
- Paste source code

### Language Detection

- Automatic language identification
- Python detection
- Java detection

### Syntax Validation

- Python syntax validation
- Java syntax validation
- Error reporting

### Knowledge Base

- Load PDF documents
- Split documents into chunks
- Generate embeddings
- Store vectors in ChromaDB

---

# 📦 Dependencies

- Streamlit
- LangChain
- LangChain Community
- LangChain Chroma
- LangChain HuggingFace
- LangChain Text Splitters
- ChromaDB
- Sentence Transformers
- PyPDF
- Python Dotenv
- Javalang
- Groq

---

# 📄 License

This project is intended for educational and learning purposes.
