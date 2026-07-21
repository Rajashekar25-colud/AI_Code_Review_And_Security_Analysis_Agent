# 🤖 AI Code Review & Security Analysis Agent

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](https://img.shields.io/badge/AI-RAG%20Powered-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Project-Milestone%202%20Completed-success)

An AI-powered static code analysis platform that automatically reviews source code for **syntax errors, code quality issues, and security vulnerabilities** using Artificial Intelligence, Retrieval-Augmented Generation (RAG), and OWASP secure coding knowledge.

---

# 🔗 Project Links

## GitHub Repository

https://github.com/Rajashekar25-colud/AI_Code_Review_And_Security_Analysis_Agent

## Live Demo

https://aicodereviewandsecurityanalysisagent-nhndxuyepv8368zmzk39kx.streamlit.app/

---

# 📌 Project Overview

The **AI Code Review & Security Analysis Agent** is an intelligent static code analysis system developed using:

- Python
- Streamlit
- LangChain
- HuggingFace Embeddings
- ChromaDB
- RAG (Retrieval-Augmented Generation)

The system automatically analyzes **Python and Java source code** and generates a detailed review report containing:

- Syntax validation results
- Code quality analysis
- Security vulnerability detection
- OWASP-based security recommendations
- Severity classification
- Secure coding suggestions

The main objective of this project is to help developers identify software defects and security risks before deploying applications into production.

---

# 🎯 Objectives

- Automate source code review using AI
- Detect common programming mistakes
- Identify security vulnerabilities
- Provide OWASP-based recommendations
- Reduce manual code review effort
- Improve secure software development practices

---

# ✨ Features

# 📂 1. Code Submission Module

The application supports:

- Upload Python files (`.py`)
- Upload Java files (`.java`)
- Paste source code directly
- Automatic programming language detection


---

# ✅ 2. Syntax Validation

## Python

Features:

- Python syntax checking
- Error detection
- Error reporting


## Java

Features:

- Java syntax validation
- Java parsing using `javalang`
- Syntax error reporting


---

# 🔍 3. Code Quality Analysis Agent

The Code Analysis Agent identifies programming issues and code smells.

## Detected Issues

### Code Smells

- Console output statements
- Long methods
- Long lines
- Too many parameters
- Magic numbers
- TODO/FIXME comments
- Duplicate imports
- Unused imports
- Global variables
- Deep nesting


### Exception Handling Problems

- Bare except blocks
- Generic exception handling
- Empty exception blocks


### Logic Issues

- Infinite loops
- Poor coding practices


---

# 🔒 4. Security Vulnerability Detection Agent

The Security Agent detects OWASP-related vulnerabilities.

## Supported Security Checks

| Vulnerability | Severity |
|---|---|
| SQL Injection | High |
| Hardcoded Secrets | High |
| Command Injection | Critical |
| Path Traversal | High |
| Cross-Site Scripting (XSS) | Medium |
| Weak Cryptography | Medium |
| Insecure Deserialization | High |
| Weak Password Handling | Medium |
| Weak Random Number Generation | Medium |


Each vulnerability report contains:

- Vulnerability name
- Severity level
- Description
- Recommendation


---

# 📚 5. Secure Coding Knowledge Base (RAG)

The project uses Retrieval-Augmented Generation to provide secure coding recommendations.

The knowledge base contains security documents including:

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

# 🏗 System Architecture


```
                  User Source Code
                         |
                         ▼
             Language Detection Module
                         |
                         ▼
             Syntax Validation Module
                         |
                         ▼
              Code Analysis Agent
                         |
                         ▼
            Security Analysis Agent
                         |
                         ▼
              RAG Knowledge Retrieval
                         |
                         ▼
             Consolidated Review Report

```

---

# 🔄 RAG Pipeline


```
          Secure Coding Documents (PDF)
                         |
                         ▼
                    PDF Loader
                         |
                         ▼
                  Text Splitter
                         |
                         ▼
            HuggingFace Embedding Model
                         |
                         ▼
              Chroma Vector Database
                         |
                         ▼
              Similarity Search
                         |
                         ▼
             Relevant Context Retrieval
                         |
                         ▼
           Secure Coding Recommendations

```

---

# 🛠 Technology Stack


## Frontend

- Streamlit


## Backend

- Python


## AI / RAG

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
├── LICENSE
├── README.md
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


## 1. Clone Repository

```bash
git clone https://github.com/Rajashekar25-colud/AI_Code_Review_And_Security_Analysis_Agent.git
```


## 2. Navigate to Project

```bash
cd AI_Code_Review_And_Security_Analysis_Agent
```


## 3. Install Dependencies

```bash
pip install -r requirements.txt
```


---

# 🔑 Environment Configuration


Create a `.env` file in the project root.


```
GROQ_API_KEY=your_groq_api_key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DB=chroma_db

KNOWLEDGE_BASE=knowledge_base

UPLOAD_FOLDER=uploads

```


---

# ▶ Run Application


```bash
streamlit run app.py
```


The application will start locally:

```
http://localhost:8501
```

---

# 📊 Analysis Dashboard


The dashboard provides:

✅ Language Detection  
✅ Syntax Validation  
✅ Code Quality Findings  
✅ Security Vulnerability Findings  
✅ Severity Classification  
✅ Recommendations  
✅ Consolidated Review Report  


## Severity Levels


🔴 Critical  
🟠 High  
🟡 Medium  
🟢 Low  


---

# 🧪 Functional Modules


## Code Submission

- Upload source files
- Paste source code
- Automatic language detection


## Syntax Analysis

- Python syntax validation
- Java syntax validation


## Code Review

- Code smell detection
- Programming practice analysis
- Maintainability checks


## Security Review

- OWASP vulnerability detection
- Secure coding recommendations


## Knowledge Base

- PDF document loading
- Text extraction
- Document splitting
- Embedding generation
- Vector storage
- Similarity search


---

# 📦 Dependencies


Main libraries:

```
streamlit
langchain
langchain-community
langchain-chroma
langchain-huggingface
chromadb
sentence-transformers
pypdf
python-dotenv
javalang
groq
```

---

# 🚀 Future Enhancements


Future improvements planned:

- AI-generated code fixes
- PDF report generation
- HTML security reports
- User authentication
- Analysis history
- GitHub Pull Request integration
- CI/CD security scanning
- SonarQube-style dashboard
- Additional OWASP security rules


---

# 📈 Project Status


✅ Milestone 1 Completed  
✅ Milestone 2 Completed  
✅ AI Agents Implemented  
✅ RAG Knowledge Base Integrated  
✅ Streamlit Deployment Completed  
✅ MIT License Added  


The project is ready for academic evaluation and final demonstration.


---

# 👨‍💻 Developer


**Rajashekar Kanneboina**

B.Tech - Computer Science & Engineering

Marri Laxman Reddy Institute of Technology and Management (MLRITM)

Hyderabad, India


---

# 📄 License


This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.


---
## 📁 Milestone Documentation

The **Milestone docs** folder contains supporting documentation for the project:

- 📅 Agile Template
- 🧪 Unit Test Plan
- 🐞 Defect Tracker

# 📄 PDF Report Generation

After completing code analysis, users can download a professional PDF report containing:

- Project title
- Programming language
- File name
- Severity summary
- Code quality findings
- Security vulnerabilities
- Line numbers
- Recommendations

# ⭐ Acknowledgements


- OWASP Foundation for security guidelines
- LangChain community
- HuggingFace community
- Streamlit community
