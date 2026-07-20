# 🤖 AI Code Review & Security Analysis Agent

## 🔗 GitHub Repository
https://github.com/Rajashekar25-colud/AI_Code_Review_And_Security_Analysis_Agent

## 🌐 Live Demo
https://aicodereviewandsecurityanalysisagent-nhndxuyepv8368zmzk39kx.streamlit.app/

---

# 📌 Project Overview

The **AI Code Review & Security Analysis Agent** is an AI-powered static code analysis platform developed using **Python**, **Streamlit**, **LangChain**, **HuggingFace Embeddings**, and **ChromaDB**.

The application automatically analyzes **Python** and **Java** source code for:

- Syntax Validation
- Code Quality Analysis
- Security Vulnerability Detection
- OWASP-Based Secure Coding Review
- Retrieval-Augmented Generation (RAG) Knowledge Base

The system helps developers identify coding issues, security vulnerabilities, and secure coding best practices before deployment.

---

# ✨ Features

## 📂 Code Submission

- Upload Python (.py) files
- Upload Java (.java) files
- Paste source code directly
- Automatic language detection

---

## ✅ Syntax Validation

### Python

- Syntax checking
- Error reporting

### Java

- Syntax validation using javalang
- Error reporting

---

# 🔍 Code Quality Analysis

The Code Analysis Agent detects:

- Console Output Statements
- Long Methods
- Long Lines
- Too Many Parameters
- Magic Numbers
- TODO / FIXME Comments
- Duplicate Imports
- Unused Imports
- Global Variables
- Bare Except Blocks
- Generic Exception Catch
- Empty Exception Blocks
- Infinite Loops
- Deep Nesting

---

# 🔒 Security Vulnerability Detection

The Security Agent detects OWASP-related vulnerabilities including:

- SQL Injection
- Hardcoded Secrets
- Weak Passwords
- Command Injection
- Path Traversal
- Cross-Site Scripting (XSS)
- Weak Cryptography
- Insecure Deserialization
- Weak Random Number Generation

Each vulnerability includes:

- Severity
- Description
- Recommendation

---

# 📚 Secure Coding Knowledge Base (RAG)

The application builds a searchable knowledge base from secure coding documents.

Included documents:

- OWASP Top 10
- OWASP Top 10 2025
- SQL Injection
- Broken Access Control
- Weak Authentication
- Security Misconfiguration
- Cryptographic Failures
- Insecure Design
- Logging & Monitoring
- Vulnerable Components
- SSRF
- SSL Security
- XML Security
- Java Secure Coding
- Python Security Considerations
- Python Secrets Module
- Secure Coding Guide
- Pickle Security
- Subprocess Security

---

# 🛠 Tech Stack

## Frontend

- Streamlit

## Backend

- Python

## AI & RAG

- LangChain
- HuggingFace Embeddings
- ChromaDB

## Document Processing

- PyPDF

## Programming Languages Supported

- Python
- Java

---

# 📂 Project Structure

```
AI-Code-Review-Agent/
│
├── app.py
├── requirements.txt
├── .env
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── code_analysis_agent.py
│   └── security_agent.py
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
├── knowledge_base/
│
├── chroma_db/
│
└── uploads/
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/Rajashekar25-colud/AI_Code_Review_And_Security_Analysis_Agent.git
```

---

## Navigate to Project

```bash
cd AI_Code_Review_And_Security_Analysis_Agent
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a **.env** file in the project root.

```text
GROQ_API_KEY=your_groq_api_key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DB=chroma_db

KNOWLEDGE_BASE=knowledge_base

UPLOAD_FOLDER=uploads
```

---

## Run the Application

```bash
streamlit run app.py
```

---

# 🏗 System Workflow

```
             User Source Code
                    │
                    ▼
         Language Detection Module
                    │
                    ▼
           Syntax Validation Module
                    │
                    ▼
        Code Analysis Agent
                    │
                    ▼
        Security Analysis Agent
                    │
                    ▼
      Severity Classification
                    │
                    ▼
      Consolidated Review Report
```

---

# 📚 RAG Pipeline

```
Knowledge Base PDFs
          │
          ▼
    PDF Loader
          │
          ▼
    Text Splitter
          │
          ▼
 HuggingFace Embeddings
          │
          ▼
 Chroma Vector Database
          │
          ▼
   Similarity Search
          │
          ▼
 Context Retrieval
```

---

# 📊 Analysis Dashboard

The application provides:

- Language Detection
- Syntax Validation
- Code Analysis Findings
- Security Findings
- Severity Summary
- Recommendations
- Consolidated Review Report

Severity Levels:

- 🔴 Critical
- 🟠 High
- 🟡 Medium
- 🟢 Low

---

# 🧪 Functionalities

## Code Submission

- Upload Python Files
- Upload Java Files
- Paste Source Code

---

## Language Detection

- Automatic Detection
- Python
- Java

---

## Syntax Validation

- Python Syntax Validation
- Java Syntax Validation

---

## Code Analysis

- Console Output Detection
- Long Method Detection
- Long Line Detection
- Too Many Parameters
- Magic Numbers
- Duplicate Imports
- Unused Imports
- Global Variables
- TODO/FIXME Comments
- Infinite Loop Detection
- Deep Nesting Detection
- Bare Exception Detection
- Generic Exception Detection
- Empty Exception Blocks

---

## Security Analysis

- SQL Injection
- Hardcoded Secrets
- Weak Password Detection
- Command Injection
- Path Traversal
- Cross Site Scripting (XSS)
- Weak Cryptography
- Insecure Deserialization
- Weak Random Number Generation

---

## Knowledge Base

- Load Secure Coding PDFs
- Split Documents
- Generate Embeddings
- Store in ChromaDB
- Retrieve Relevant Context

---

# 📦 Dependencies

- streamlit
- langchain
- langchain-community
- langchain-chroma
- langchain-huggingface
- chromadb
- sentence-transformers
- pypdf
- python-dotenv
- javalang
- groq

---

# 🚀 Future Enhancements

- AI-generated Fix Suggestions
- PDF Report Export
- HTML Report Export
- Analysis History
- User Authentication
- GitHub Pull Request Integration
- SonarQube-style Dashboard
- Additional OWASP Rules
- CI/CD Integration

---

# 👨‍💻 Developer

**Rajashekar Kanneboina**

B.Tech – Computer Science & Engineering

Marri Laxman Reddy Institute of Technology and Management (MLRITM)

Hyderabad, India

---

# 📄 License

This project is developed for educational and learning purposes.