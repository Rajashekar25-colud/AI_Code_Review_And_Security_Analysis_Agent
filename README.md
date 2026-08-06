# 🤖 AI Code Review & Security Analysis Agent

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Java](https://img.shields.io/badge/Java-Supported-orange)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-success)
![Groq](https://img.shields.io/badge/LLM-Groq-purple)
![RAG](https://img.shields.io/badge/RAG-Enabled-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📌 Project Title

## AI Code Review & Security Analysis Agent

An intelligent **AI-powered multi-agent platform** that automatically reviews **Python** and **Java** source code for:

- Code Quality Issues
- Security Vulnerabilities
- OWASP Violations
- Secure Coding Practices
- AI-powered Remediation
- Pull Request Review Summary
- RAG-powered Conversational Assistant

---

# 📖 Project Overview

Modern software projects grow rapidly, making manual code reviews slow, inconsistent, and difficult to scale.

Developers often miss:

- Security vulnerabilities
- Code smells
- Maintainability issues
- OWASP violations
- Best coding practices

Our project automates the review process using **AI Agents**, **Static Analysis Tools**, and **Retrieval-Augmented Generation (RAG)**.

The system supports both **Python** and **Java** and generates professional review reports with explanations and secure coding recommendations.

---

# 🎯 Problem Statement

Manual code reviews have several challenges:

- Time-consuming
- Human errors
- Inconsistent reviews
- Late vulnerability detection
- Lack of secure coding guidance

This project solves these problems by automatically analyzing source code and providing AI-powered feedback before deployment.

---

# 🎯 Objectives

The main objectives of this project are:

### ✅ Automated Code Review

Analyze Python and Java source code automatically.

### ✅ Security Analysis

Detect OWASP Top 10 vulnerabilities.

### ✅ AI Remediation

Generate secure coding recommendations with corrected code examples.

### ✅ PR Summary Generation

Produce a professional pull-request style review.

### ✅ Conversational Assistant

Allow developers to ask follow-up questions using a RAG-powered chatbot grounded in secure coding documents.

---

# ✨ Key Features

- Upload Python (.py) and Java (.java) files
- Paste source code directly
- Automatic language detection
- Syntax validation
- Code quality analysis
- Security vulnerability detection
- AI-generated remediation
- Pull Request summary
- Severity scoring
- Overall code health score
- Analytics dashboard
- PDF report generation
- RAG-powered conversational assistant

---
## 🏗️ System Architecture

```text
                           👨‍💻 Developer
                                 │
          Paste Code / Upload Python or Java File
                                 │
                                 ▼
                   ┌─────────────────────────┐
                   │ Code Submission Module  │
                   └─────────────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────┐
                 │ Language Detection         │
                 │ Syntax Validation          │
                 └────────────────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────┐
                 │ LangGraph Orchestrator     │
                 │ Coordinates All Agents     │
                 └────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                ▼                                 ▼
     ┌────────────────────────┐      ┌────────────────────────┐
     │ Code Analysis Agent    │      │ Security Agent         │
     ├────────────────────────┤      ├────────────────────────┤
     │ • PMD                  │      │ • Bandit              │
     │ • Checkstyle           │      │ • SpotBugs            │
     │ • Pylint               │      │ • OWASP Rules         │
     │ • Radon                │      │ • Custom Rules        │
     │ • Custom Quality Rules │      └────────────────────────┘
     └────────────────────────┘
                │                         │
                └────────────┬────────────┘
                             ▼
             ┌────────────────────────────────┐
             │ Unified Findings Repository    │
             └────────────────────────────────┘
                             │
                             ▼
             ┌────────────────────────────────┐
             │ Remediation Agent              │
             │ • Fix Recommendations          │
             │ • Secure Coding Practices      │
             │ • Corrected Code Examples      │
             └────────────────────────────────┘
                             │
                             ▼
             ┌────────────────────────────────┐
             │ PR Summary Agent               │
             │ • Executive Summary            │
             │ • Severity Breakdown           │
             │ • Code Health Score            │
             └────────────────────────────────┘
                             │
                             ▼
             ┌────────────────────────────────┐
             │ Streamlit Developer Portal     │
             │ • Findings                     │
             │ • Dashboard                    │
             │ • Analytics                    │
             │ • PDF Report                   │
             └────────────────────────────────┘
                             │
                             ▼
             ┌────────────────────────────────┐
             │ Conversational Code Assistant  │
             │ (Groq LLM + LangChain + RAG)   │
             └────────────────────────────────┘
                             │
                             ▼
             ┌────────────────────────────────┐
             │ Secure Coding Knowledge Base   │
             │ • OWASP Top 10                 │
             │ • Java Secure Coding           │
             │ • Python Guidelines            │
             │ • Best Practices               │
             │ • ChromaDB Vector Database     │
             └────────────────────────────────┘
```


## 📂 Project Structure

```text
AI-Code-Review-Agent/
│
├── app.py                          # Streamlit entry point
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation
├── .env                            # Environment variables
│
├── agents/
│   ├── orchestrator.py             # Coordinates all AI agents
│   ├── code_analysis_agent.py      # Code quality analysis
│   ├── security_agent.py           # Security vulnerability detection
│   ├── remediation_agent.py        # Generates fix recommendations
│   ├── pr_summary_agent.py         # Creates PR review summary
│   ├── conversational_assistant.py # RAG-powered AI assistant
│   └── java_security_analyzer.py   # Java-specific security analysis
│
├── modules/
│   ├── submission.py               # Code submission handling
│   ├── language_detector.py        # Python/Java detection
│   ├── syntax_validator.py         # Syntax validation
│   ├── java_compiler.py            # Java compilation
│   ├── report_generator.py         # PDF report generation
│   └── file_handler.py             # File upload handling
│
├── tools/
│   ├── pylint_runner.py            # Python quality analysis
│   ├── radon_runner.py             # Complexity analysis
│   ├── bandit_runner.py            # Python security scanner
│   ├── pmd_runner.py               # Java quality analysis
│   ├── checkstyle_runner.py        # Java coding standards
│   ├── spotbugs_runner.py          # Java bug detection
│   ├── java_security_scanner.py    # Java security scanner
│   ├── java_quality_analyzer.py    # Java quality analyzer
│   └── python_security_scanner.py  # Python security scanner
│
├── rag/
│   ├── loader.py                   # Loads knowledge documents
│   ├── splitter.py                 # Splits documents into chunks
│   ├── embedding.py                # Generates embeddings
│   ├── vector_store.py             # ChromaDB vector storage
│   ├── build_knowledgebase.py      # Builds RAG knowledge base
│   └── groq_model.py               # Groq LLM integration
│
├── ui/
│   ├── review_page.py              # Code review page
│   ├── assistant.py                # AI chat assistant
│   ├── analytics.py                # Analytics dashboard
│   ├── dashboard.py                # Main dashboard
│   ├── reports.py                  # Report viewer
│   ├── history.py                  # Review history
│   ├── sidebar.py                  # Navigation sidebar
│   └── settings.py                 # Application settings
│
├── knowledge_base/                 # OWASP & secure coding documents
├── generated_reports/              # Generated PDF reports
└── chroma_db/                      # ChromaDB vector database
```


# 🤖 Multi-Agent Architecture

The system follows a **Multi-Agent Architecture**, where each AI agent performs one specific responsibility.

---

## 1️⃣ LangGraph Orchestrator Agent

**Responsibility**

Acts as the central controller.

### Tasks

- Receives validated source code
- Starts analysis workflow
- Coordinates all agents
- Collects results
- Passes outputs to next agent

---

## 2️⃣ Code Analysis Agent

This agent focuses on **code quality**.

### Detects

- Unused Variables
- Unused Imports
- Duplicate Imports
- Long Methods
- Long Lines
- Magic Numbers
- Duplicate Code
- Dead Code
- Empty Catch Blocks
- Deep Nesting
- Console Logging
- Poor Exception Handling
- Complexity Issues

### Tools Used

- PMD
- Checkstyle
- Pylint
- Radon
- Custom Rules

---

## 3️⃣ Security Agent

Responsible for detecting security vulnerabilities.

### Detects

- SQL Injection
- Command Injection
- Hardcoded Secrets
- Weak Authentication
- Broken Access Control
- Path Traversal
- XXE Injection
- Insecure Deserialization
- Weak Random Numbers
- Weak Cryptography
- Cross Site Scripting (XSS)

### Tools Used

- Bandit
- SpotBugs
- Custom Security Scanner
- OWASP Rules

---

## 4️⃣ Remediation Agent

After all findings are collected, the Remediation Agent generates secure fixes.

### Generates

- Secure Coding Recommendations
- Corrected Code Examples
- Best Practices
- OWASP Guidance
- Refactoring Suggestions

Powered by:

- Groq LLM

---

## 5️⃣ PR Summary Agent

Creates a professional Pull Request Review.

Includes

- Executive Summary
- Code Health Score
- Severity Breakdown
- Priority Fixes
- Final Recommendation

Powered by

- Groq LLM

---

## 6️⃣ Conversational Code Assistant

Allows developers to ask follow-up questions after code review.

Examples

- Why is SQL Injection dangerous?
- Explain XXE Attack.
- Show secure Java code.
- Explain OWASP recommendations.

This assistant uses

- LangChain
- Groq LLM
- ChromaDB
- RAG Knowledge Base

---

# 📚 Secure Coding Knowledge Base (RAG)

Instead of answering from memory, the assistant retrieves information from an indexed secure coding knowledge base.

Knowledge Sources

- OWASP Top 10
- Java Secure Coding Guidelines
- Python Secure Coding Guidelines
- Secure Coding Best Practices
- Internal Documentation

Pipeline

```
Documents

      │

      ▼

Document Loader

      │

      ▼

Text Splitter

      │

      ▼

Embeddings

(sentence-transformers)

      │

      ▼

ChromaDB Vector Store

      │

      ▼

Retriever

      │

      ▼

Groq LLM

      │

      ▼

Final Answer
```

---

# 💻 Technology Stack

| Category | Technology |
|------------|----------------|
| Programming | Python, Java |
| Frontend | Streamlit |
| AI Framework | LangChain |
| Multi-Agent | LangGraph |
| LLM | Groq |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers |
| Python Security | Bandit |
| Python Quality | Pylint, Radon |
| Java Quality | PMD, Checkstyle |
| Java Security | SpotBugs |
| Java Parser | javalang |
| Report Generation | ReportLab |
| Charts | Plotly, Pandas |

---

# ⚙️ Workflow

```
Developer

     │

Paste Code / Upload File

     │

Language Detection

     │

Syntax Validation

     │

LangGraph Orchestrator

     │

Code Analysis Agent

     │

Security Agent

     │

Unified Findings

     │

Remediation Agent

     │

PR Summary Agent

     │

Developer Dashboard

     │

PDF Report

     │

Conversational AI Assistant
```

---

# 📊 Severity Levels

| Severity | Meaning |
|-----------|----------|
| 🔴 Critical | Immediate security risk |
| 🟠 High | Serious vulnerability |
| 🟡 Medium | Moderate issue |
| 🔵 Low | Minor issue |
| 🟢 Info | Recommendation |

---

# 📄 Generated Report Includes

The generated PDF report contains:

- Executive Summary
- Code Health Score
- Severity Breakdown
- Quality Issues
- Security Findings
- AI Remediation Suggestions
- Corrected Code Examples
- Pull Request Summary
- Overall Recommendation
# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Code-Review-Agent.git
cd AI-Code-Review-Agent
```

---

## 2. Create Virtual Environment

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

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 5. Build the RAG Knowledge Base

```bash
python rag/build_knowledgebase.py
```

This indexes:

- OWASP Top 10
- Java Secure Coding Guidelines
- Python Secure Coding Guidelines
- Secure Coding Best Practices

into the ChromaDB vector database.

---

## 6. Run the Application

```bash
streamlit run app.py
```

The application opens in your browser.

---

# 💻 Application Modules

## 1. Code Submission Module

Supports:

- Paste Python code
- Paste Java code
- Upload `.py`
- Upload `.java`

---

## 2. Language Detection Module

Automatically detects:

- Python
- Java

---

## 3. Syntax Validation Module

Checks whether submitted code is syntactically correct before analysis.

---

## 4. Multi-Agent Analysis Module

Performs:

- Code Quality Review
- Security Analysis
- Remediation
- PR Summary Generation

---

## 5. Findings Dashboard

Displays:

- Severity Score
- Health Score
- Security Findings
- Quality Findings
- AI Recommendations

---

## 6. PDF Report Module

Generates downloadable reports containing:

- Executive Summary
- Security Findings
- Code Quality Findings
- Remediation
- PR Summary
- Overall Recommendation

---

## 7. Conversational Assistant

Developers can ask:

- Explain SQL Injection
- Explain XXE
- Why is this vulnerability dangerous?
- Show secure Java code
- Show secure Python example

The assistant answers using the RAG Knowledge Base.

---

# 🧪 Testing & Validation

The application was tested using intentionally vulnerable Python and Java programs.

## Security Test Cases

| Test Case | Status |
|------------|---------|
| SQL Injection | ✅ Pass |
| Command Injection | ✅ Pass |
| Hardcoded Secrets | ✅ Pass |
| Weak Authentication | ✅ Pass |
| Weak Cryptography | ✅ Pass |
| XXE Injection | ✅ Pass |
| Path Traversal | ✅ Pass |
| Insecure Deserialization | ✅ Pass |
| Weak Random Generator | ✅ Pass |

---

## Code Quality Test Cases

| Test Case | Status |
|------------|---------|
| Unused Variable | ✅ Pass |
| Unused Import | ✅ Pass |
| Duplicate Import | ✅ Pass |
| Magic Number | ✅ Pass |
| Deep Nesting | ✅ Pass |
| Empty Catch Block | ✅ Pass |
| Console Logging | ✅ Pass |
| Duplicate Code | ✅ Pass |
| Unnecessary Object Creation | ✅ Pass |
| Primitive Wrapper Instantiation | ✅ Pass |
| Dead Code | ✅ Pass |
| Poor Exception Handling | ✅ Pass |

---

# 📊 Application Output

After analysis, the application provides:

- Language Detection
- Syntax Validation
- Code Health Score
- Severity Breakdown
- Security Findings
- Code Quality Findings
- AI Remediation Suggestions
- Pull Request Summary
- Downloadable PDF Report

---

# 🌟 Advantages

- Faster than manual code review
- Detects security vulnerabilities early
- Improves code quality
- Supports Python and Java
- AI-powered remediation
- Professional PR-style review
- Interactive developer dashboard
- RAG-powered secure coding assistant
- Exportable PDF reports
- Easy-to-use web interface

---

# 🚀 Future Enhancements

Future improvements include:

- Support for C, C++, JavaScript, and Go
- GitHub Pull Request integration
- VS Code extension
- CI/CD pipeline integration
- Docker deployment
- SonarQube integration
- Email notification support
- Team collaboration dashboard
- Auto-fix suggestions
- Cloud deployment support

---

# 📈 Project Outcomes

This project successfully achieves the following outcomes:

- Automated code review using AI agents
- Detection of code quality issues
- Detection of OWASP security vulnerabilities
- AI-generated remediation suggestions
- Professional pull request summaries
- Secure coding guidance using RAG
- Interactive developer dashboard
- Exportable PDF reports

---

# 📚 References

- OWASP Top 10
- OWASP Secure Coding Practices
- Python Security Guidelines
- Java Secure Coding Guidelines
- PMD Documentation
- Checkstyle Documentation
- SpotBugs Documentation
- Bandit Documentation
- LangChain Documentation
- LangGraph Documentation
- Groq API Documentation
- ChromaDB Documentation
- Streamlit Documentation

---

# 👨‍💻 Developed By

**AI Code Review & Security Analysis Agent**

B.Tech CSE Major Project

Developed using:

- Python
- Java
- Streamlit
- LangGraph
- LangChain
- Groq LLM
- ChromaDB
- Bandit
- PMD
- Checkstyle
- SpotBugs

---

# 📄 License

This project is developed for educational and research purposes.

MIT License.

---

# ⭐ Thank You

If you found this project useful, please consider giving it a ⭐ on GitHub.

**Happy Secure Coding! 🔒💻**