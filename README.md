# 🤖 AI Code Review & Security Analysis Agent

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Java](https://img.shields.io/badge/Java-Supported-orange)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](https://img.shields.io/badge/AI-RAG%20Powered-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Milestone%202%20Completed-success)

An AI-powered static code analysis platform that automatically reviews **Python** and **Java** source code for **syntax errors**, **code quality issues**, and **security vulnerabilities** using **Artificial Intelligence (AI)**, **Retrieval-Augmented Generation (RAG)**, and **OWASP secure coding practices**.

The application helps developers identify bugs, code smells, and security risks early in the software development lifecycle while promoting secure coding standards.

---

# 🔗 Project Links

## 📂 GitHub Repository

**Repository:**  
https://github.com/Rajashekar25-colud/AI_Code_Review_And_Security_Analysis_Agent

## 🌐 Live Demo

**Streamlit Application:**  
https://aicodereviewandsecurityanalysisagent-nhndxuyepv8368zmzk39kx.streamlit.app/

---

# 📌 Project Overview

The **AI Code Review & Security Analysis Agent** is an intelligent static code analysis platform designed to automate software quality assurance and security review.

The system leverages:

- 🐍 Python
- 🎨 Streamlit
- 🤖 LangChain
- 🧠 HuggingFace Embeddings
- 🗄 ChromaDB
- 📚 Retrieval-Augmented Generation (RAG)

The application analyzes uploaded or pasted source code and generates a comprehensive review report including:

- ✅ Programming language detection
- ✅ Syntax validation
- ✅ Code quality analysis
- ✅ Security vulnerability detection
- ✅ Severity classification
- ✅ Secure coding recommendations
- ✅ Downloadable PDF report

The goal is to assist developers in writing cleaner, safer, and more maintainable code before deployment.

---

# 🎯 Project Objectives

The primary objectives of this project are:

- Automate source code review using AI
- Detect syntax errors in Python and Java
- Identify common code smells
- Detect OWASP-based security vulnerabilities
- Provide secure coding recommendations using RAG
- Reduce manual code review effort
- Improve software quality
- Promote secure software development practices

---

# ✨ Key Features

## 📂 Code Submission Module

Supports:

- Upload Python (.py) files
- Upload Java (.java) files
- Paste source code directly
- Automatic language detection

---

## ✅ Syntax Validation

### Python

- AST-based syntax validation
- Detailed syntax error reporting

### Java

- Java parsing using `javalang`
- Syntax error detection
- Validation reporting

---

## 🔍 Code Quality Analysis Agent

Automatically detects:

- Console output statements
- Long methods
- Long lines
- Too many parameters
- Magic numbers
- TODO/FIXME comments
- Duplicate imports
- Unused imports
- Global variables
- Bare exception blocks
- Generic exception handling
- Empty exception blocks
- Infinite loops
- Deep nesting
- Poor coding practices

---

## 🔒 Security Analysis Agent

The Security Agent detects common OWASP-related vulnerabilities including:

| Vulnerability | Severity |
|---------------|----------|
| SQL Injection | High |
| Hardcoded Secrets | High |
| Command Injection | Critical |
| Path Traversal | High |
| Cross-Site Scripting (XSS) | Medium |
| Weak Cryptography | Medium |
| Insecure Deserialization | High |
| Weak Password Handling | Medium |
| Weak Random Number Generation | Medium |

Each finding includes:

- Vulnerability Name
- Severity
- Description
- Recommendation

---

## 📄 PDF Report Generation

Generate a professional PDF report containing:

- Programming language
- Syntax validation results
- Code quality findings
- Security findings
- Severity summary
- Recommendations

---# 📚 Secure Coding Knowledge Base (RAG)

The application uses **Retrieval-Augmented Generation (RAG)** to provide context-aware secure coding recommendations.

Instead of relying solely on predefined rules, the system retrieves relevant information from a curated knowledge base of OWASP and secure coding documents.

## 📖 Knowledge Base Includes

The following security resources are indexed into the vector database:

- OWASP Top 10
- OWASP Top 10 2025
- SQL Injection
- Broken Access Control
- Weak Authentication
- Security Misconfiguration
- Cryptographic Failures
- Insecure Design
- Security Logging & Monitoring
- Vulnerable Components
- Server-Side Request Forgery (SSRF)
- SSL/TLS Security
- XML Security
- Java Secure Coding
- Python Security Considerations
- Python Secrets Module
- Secure Coding Guide
- Pickle Security
- Subprocess Security

These documents are processed using LangChain and stored in ChromaDB to enable semantic search and intelligent retrieval.

---

# 🤖 AI Agents

The project follows a modular multi-agent architecture.

## 🔍 Code Analysis Agent

Responsibilities:

- Detect code smells
- Identify poor coding practices
- Analyze maintainability
- Generate quality recommendations

### Detects

- Long methods
- Long lines
- Duplicate imports
- Unused imports
- TODO/FIXME comments
- Global variables
- Magic numbers
- Infinite loops
- Deep nesting
- Exception handling issues

---

## 🔒 Security Analysis Agent

Responsibilities:

- Detect security vulnerabilities
- Perform OWASP-based analysis
- Assign severity levels
- Suggest secure coding practices

### Detects

- SQL Injection
- Hardcoded API keys
- Weak passwords
- Command Injection
- Path Traversal
- Cross-Site Scripting (XSS)
- Weak cryptography
- Insecure deserialization
- Weak random number generation

---

## 🎯 Orchestrator Agent

The Orchestrator coordinates the complete review process by:

- Receiving source code
- Calling the Code Analysis Agent
- Calling the Security Analysis Agent
- Combining findings
- Generating a consolidated review report

---

# 🏗 System Architecture

```text
                    User Source Code
                           │
                           ▼
               Language Detection Module
                           │
                           ▼
                Syntax Validation Module
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
 Code Analysis Agent              Security Analysis Agent
          │                                 │
          └────────────────┬────────────────┘
                           ▼
                 Severity Classification
                           │
                           ▼
                RAG Knowledge Retrieval
                           │
                           ▼
             Consolidated Review Report
                           │
                           ▼
                 Download PDF Report
```

---

# 🔄 Application Workflow

```text
User Uploads Code
        │
        ▼
Language Detection
        │
        ▼
Syntax Validation
        │
        ▼
Code Quality Analysis
        │
        ▼
Security Vulnerability Detection
        │
        ▼
Retrieve Secure Coding Context (RAG)
        │
        ▼
Generate Review Report
        │
        ▼
Display Results in Streamlit
        │
        ▼
Download PDF Report
```

---

# 🔄 RAG Pipeline

```text
      Secure Coding PDF Documents
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
        Context Retrieval (RAG)
                    │
                    ▼
 Secure Coding Recommendations
```

---

# 📊 Output Generated

After analysis, the application generates:

- ✅ Programming Language Detection
- ✅ Syntax Validation Report
- ✅ Code Quality Analysis
- ✅ Security Vulnerability Report
- ✅ Severity Classification
- ✅ Secure Coding Recommendations
- ✅ Downloadable PDF Report
# 🛠 Technology Stack

The project is built using modern AI, Machine Learning, and Software Engineering technologies.

## 💻 Programming Languages

- Python
- Java (Supported for Analysis)

---

## 🎨 Frontend

- Streamlit

Features:

- Interactive User Interface
- File Upload
- Code Editor
- Analysis Dashboard
- PDF Report Download

---

## ⚙ Backend

- Python

Core Responsibilities:

- Language Detection
- Syntax Validation
- Code Analysis
- Security Analysis
- Report Generation
- RAG Integration

---

## 🤖 AI & RAG Technologies

- LangChain
- HuggingFace Embeddings
- ChromaDB
- Groq LLM

These technologies power the Retrieval-Augmented Generation (RAG) pipeline for secure coding recommendations.

---

## 📄 Document Processing

- PyPDF

Used for:

- Reading Secure Coding PDFs
- Knowledge Base Construction

---

## 🗄 Vector Database

- ChromaDB

Used to:

- Store Embeddings
- Similarity Search
- Retrieve Relevant Security Context

---

## 🔐 Security Knowledge Sources

The project uses industry-standard secure coding references including:

- OWASP Top 10
- OWASP Top 10 2025
- OWASP Cheat Sheets
- Python Secure Coding
- Java Secure Coding

---

# 📂 Project Structure

```text
AI_Code_Review_And_Security_Analysis_Agent/
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── code_analysis_agent.py
│   └── security_agent.py
│
├── knowledge_base/
│   ├── OWASP Top 10.pdf
│   ├── OWASP Top 10 2025.pdf
│   ├── SQL_Injection.pdf
│   ├── Broken_Access_Control.pdf
│   ├── Weak_Authentication.pdf
│   ├── Security_Misconfiguration.pdf
│   ├── Cryptographic_Failures.pdf
│   ├── Insecure_Design.pdf
│   ├── Logging_Monitoring.pdf
│   ├── Vulnerable_Components.pdf
│   ├── SSRF.pdf
│   ├── SSL_Security.pdf
│   ├── XML_Security.pdf
│   ├── Java_Secure_Coding.pdf
│   ├── Python_Security_Considerations.pdf
│   ├── Python_Secrets_Module.pdf
│   ├── Pickle_Security.pdf
│   └── Subprocess_Security.pdf
│
├── Milestone docs/
│   ├── Agile_Template_v0.1.xlsx
│   ├── Defect_Tracker_v0.1.xlsx
│   └── Unit_Test_Plan_v0.1.xlsx
│
├── modules/
│   ├── file_handler.py
│   ├── language_detector.py
│   ├── report_generator.py
│   ├── submission.py
│   └── syntax_validator.py
│
├── rag/
│   ├── build_knowledgebase.py
│   ├── embedding.py
│   ├── groq_model.py
│   ├── loader.py
│   ├── splitter.py
│   └── vector_store.py
│
├── chroma_db/
│
├── uploads/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── .env.example
```

---

# 📁 Folder Description

| Folder | Purpose |
|---------|---------|
| `agents/` | AI agents responsible for code quality and security analysis |
| `modules/` | Core application modules such as syntax validation and report generation |
| `rag/` | Retrieval-Augmented Generation pipeline implementation |
| `knowledge_base/` | Secure coding reference documents |
| `Milestone docs/` | Agile planning and testing documentation |
| `uploads/` | Stores uploaded source code files |
| `chroma_db/` | Chroma vector database for RAG |

---

# ⚙ Core Modules

## Language Detection Module

Automatically identifies:

- Python
- Java

---

## Syntax Validator

Responsible for:

- Python syntax validation
- Java syntax validation
- Error reporting

---

## Code Analysis Agent

Performs:

- Code smell detection
- Maintainability analysis
- Programming practice evaluation

---

## Security Analysis Agent

Performs:

- Vulnerability detection
- Severity classification
- Secure coding recommendations

---

## Report Generator

Generates:

- Professional PDF Analysis Reports
- Severity Summary
- Security Findings
- Recommendations

---

## RAG Engine

Responsible for:

- Loading PDFs
- Splitting Documents
- Generating Embeddings
- Storing Vectors
- Semantic Search
- Context Retrieval

---

# 📦 Dependencies

Major Python packages used in the project:

```text
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
reportlab
groq
```

---

# 📋 System Requirements

## Software Requirements

- Python 3.11+
- Visual Studio Code
- Git
- Streamlit
- Internet Connection (for LLM API)

---

## Hardware Requirements

Minimum:

- 4 GB RAM
- Dual-Core Processor
- 2 GB Free Disk Space

Recommended:

- 8 GB RAM or above
- Quad-Core Processor
- SSD Storage

---# 🚀 Installation Guide

Follow the steps below to set up and run the project locally.

---

## 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/Rajashekar25-colud/AI_Code_Review_And_Security_Analysis_Agent.git
```

---

## 📂 Step 2: Navigate to the Project Folder

```bash
cd AI_Code_Review_And_Security_Analysis_Agent
```

---

## 🐍 Step 3: Create a Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Step 5: Configure Environment Variables

Create a file named **`.env`** in the project root directory.

Example:

```text
GROQ_API_KEY=your_groq_api_key

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DB=chroma_db

KNOWLEDGE_BASE=knowledge_base

UPLOAD_FOLDER=uploads
```

> **Note:** Replace `your_groq_api_key` with your own Groq API key.

---

## 📚 Step 6: Build the Knowledge Base (First Run Only)

Before launching the application for the first time, build the vector database.

```bash
python rag/build_knowledgebase.py
```

This step:

- Loads secure coding PDF documents
- Splits documents into chunks
- Generates embeddings
- Stores vectors in ChromaDB

After the knowledge base has been created once, you do **not** need to rebuild it unless new documents are added.

---

## ▶ Step 7: Run the Application

```bash
streamlit run app.py
```

The application will start locally at:

```
http://localhost:8501
```

---

# 🌐 Live Demo

Try the deployed application here:

**https://aicodereviewandsecurityanalysisagent-nhndxuyepv8368zmzk39kx.streamlit.app/**

---

# 💻 How to Use

## Step 1

Launch the Streamlit application.

---

## Step 2

Upload a **Python (.py)** or **Java (.java)** file,

**OR**

Paste source code directly into the editor.

---

## Step 3

The application automatically performs:

- Programming Language Detection
- Syntax Validation
- Code Quality Analysis
- Security Vulnerability Detection

---

## Step 4

View the generated analysis report including:

- Language Detected
- Syntax Status
- Code Quality Findings
- Security Findings
- Severity Summary
- Secure Coding Recommendations

---

## Step 5

Click the **Download PDF Report** button to save the complete analysis report.

---

# 📊 Analysis Dashboard

The Streamlit dashboard displays:

- 📂 File Upload
- 🌐 Language Detection
- ✅ Syntax Validation
- 🔍 Code Quality Analysis
- 🔒 Security Analysis
- 📚 RAG Recommendations
- 📄 PDF Report Download

---

# 📸 Application Screenshots

> Screenshots can be added later.

Suggested folder structure:

```text
screenshots/
│
├── home_page.png
├── upload_page.png
├── syntax_validation.png
├── code_analysis.png
├── security_analysis.png
├── pdf_report.png
```

Example:

```markdown
## Home Page

![Home](screenshots/home_page.png)

---

## Code Analysis

![Code Analysis](screenshots/code_analysis.png)

---

## Security Analysis

![Security](screenshots/security_analysis.png)

---

## PDF Report

![PDF Report](screenshots/pdf_report.png)
```

---

# 📄 Sample Workflow

```text
Upload Source Code
        │
        ▼
Language Detection
        │
        ▼
Syntax Validation
        │
        ▼
Code Quality Analysis
        │
        ▼
Security Analysis
        │
        ▼
Retrieve Secure Coding Context
        │
        ▼
Generate Analysis Report
        │
        ▼
Download PDF Report
```

---

# 💡 Tips

- Upload valid Python or Java source files.
- Larger files may take slightly longer to analyze.
- Rebuild the knowledge base only after adding or updating PDF documents.
- Keep your `.env` file private and never commit API keys to GitHub.

---# 📊 Analysis Output

After processing the uploaded source code, the application generates a comprehensive analysis report.

The report includes:

- ✅ Programming Language Detection
- ✅ Syntax Validation Status
- ✅ Code Quality Findings
- ✅ Security Vulnerability Findings
- ✅ Severity Classification
- ✅ Secure Coding Recommendations
- ✅ Downloadable PDF Report

---

# 🚦 Severity Levels

The application classifies detected issues into different severity levels.

| Severity | Description |
|----------|-------------|
| 🔴 Critical | Immediate action required. High-risk security vulnerability. |
| 🟠 High | Serious issue that should be fixed before deployment. |
| 🟡 Medium | Moderate issue affecting maintainability or security. |
| 🟢 Low | Minor issue or coding best practice recommendation. |

---

# 🧩 Functional Modules

The application is divided into multiple modules, each responsible for a specific task.

## 📂 Code Submission

Features:

- Upload Python files
- Upload Java files
- Paste source code
- Automatic language detection

---

## 🌐 Language Detection

Automatically identifies the programming language based on uploaded files or pasted source code.

Supported languages:

- Python
- Java

---

## ✅ Syntax Validation

The syntax validation module verifies source code before further analysis.

### Python

- AST-based syntax validation
- Detailed error reporting

### Java

- Syntax validation using `javalang`
- Error reporting

---

## 🔍 Code Quality Analysis

The Code Analysis Agent detects:

- Console output statements
- Long methods
- Long lines
- Too many parameters
- Magic numbers
- Duplicate imports
- Unused imports
- TODO/FIXME comments
- Global variables
- Deep nesting
- Infinite loops
- Poor coding practices
- Bare exception blocks
- Generic exception handling
- Empty exception blocks

---

## 🔒 Security Analysis

The Security Agent identifies common software security vulnerabilities including:

- SQL Injection
- Command Injection
- Hardcoded Secrets
- Weak Password Handling
- Path Traversal
- Cross-Site Scripting (XSS)
- Weak Cryptography
- Insecure Deserialization
- Weak Random Number Generation

Each finding includes:

- Vulnerability Name
- Severity
- Description
- Recommendation

---

## 📚 Secure Coding Knowledge Base

The RAG module provides intelligent recommendations using indexed secure coding documents.

Capabilities:

- Load PDF documents
- Split text into chunks
- Generate embeddings
- Store vectors in ChromaDB
- Retrieve relevant secure coding guidance
- Generate context-aware recommendations

---

## 📄 PDF Report Generator

The application allows users to download a professional analysis report in PDF format.

The report contains:

- Project Title
- Programming Language
- File Name
- Syntax Validation Result
- Code Quality Findings
- Security Vulnerabilities
- Severity Summary
- Recommendations

---

# 📁 Milestone Documentation

The **Milestone docs** folder contains project planning and testing artifacts.

| Document | Description |
|----------|-------------|
| Agile_Template_v0.1.xlsx | Sprint planning and Agile task management |
| Unit_Test_Plan_v0.1.xlsx | Unit test cases and expected results |
| Defect_Tracker_v0.1.xlsx | Defect logging and issue tracking |

---

# 🚀 Future Enhancements

Future improvements planned for the project include:

- AI-powered automatic code fix suggestions
- HTML report generation
- User authentication and role management
- Analysis history and report storage
- GitHub Pull Request integration
- CI/CD pipeline integration
- SonarQube-style analytics dashboard
- Support for additional programming languages
- Expanded OWASP security rules
- Performance optimization for large codebases

---

# 📈 Project Status

| Component | Status |
|-----------|--------|
| Streamlit Application | ✅ Completed |
| Python Syntax Validation | ✅ Completed |
| Java Syntax Validation | ✅ Completed |
| Code Analysis Agent | ✅ Completed |
| Security Analysis Agent | ✅ Completed |
| RAG Knowledge Base | ✅ Completed |
| ChromaDB Integration | ✅ Completed |
| PDF Report Generation | ✅ Completed |
| Streamlit Cloud Deployment | ✅ Completed |
| MIT License | ✅ Added |
| Milestone Documentation | ✅ Added |

The project is ready for:

- 🎓 College Project Submission
- 💼 Portfolio Showcase
- 🚀 GitHub Portfolio
- 📑 Final Demonstration
- 🎤 Viva Examination

------

# 🤝 Contributing

Contributions, suggestions, and feedback are welcome.

If you'd like to contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Please ensure your contributions follow the project's coding standards and include appropriate documentation.

---

# 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for more information.

---

# 🙏 Acknowledgements

Special thanks to the following open-source projects and communities:

- OWASP Foundation
- Streamlit
- LangChain
- Hugging Face
- ChromaDB
- Groq
- PyPDF
- Python Community
- Java Community

Their tools and documentation made this project possible.

---

# ⭐ Support

If you found this project useful, consider:

- ⭐ Starring the repository
- 🍴 Forking the project
- 🐛 Reporting issues
- 💡 Suggesting improvements
- 🤝 Contributing to future development

Your support is greatly appreciated.

---

# 🎯 Project Status

✅ Milestone 1 Completed

✅ Milestone 2 Completed

✅ AI Code Analysis Agent Implemented

✅ Security Analysis Agent Implemented

✅ RAG Knowledge Base Integrated

✅ PDF Report Generation

✅ Streamlit Cloud Deployment

✅ MIT Licensed

---

**Built to demonstrate AI-powered static code analysis, secure coding practices, and Retrieval-Augmented Generation (RAG) for educational and portfolio purposes.**