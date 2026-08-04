# 🤖 AI Code Review & Security Analysis Agent


![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Java](https://img.shields.io/badge/Java-Supported-orange)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](https://img.shields.io/badge/AI-RAG%20Powered-purple)
![LangGraph](https://img.shields.io/badge/Agent-LangGraph-green)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Milestone%203%20Completed-success)


# 📌 Project Title

# AI Code Review & Security Analysis Agent


---

# 📖 Project Overview


Software development teams frequently face challenges such as:

- Inconsistent code quality
- Undetected security vulnerabilities
- Time-consuming manual code reviews
- Lack of secure coding guidance
- Difficulty maintaining large codebases


Traditional manual code reviews are:

- Slow
- Subjective
- Difficult to scale
- Dependent on developer expertise


The **AI Code Review & Security Analysis Agent** is an intelligent multi-agent platform designed to automatically analyze source code and provide AI-powered code review assistance.


The system analyzes:

- Python source code
- Java source code


and identifies:


### 🔍 Code Quality Issues

- Code smells
- Poor coding practices
- Maintainability problems
- Design issues


### 🔒 Security Vulnerabilities

- OWASP Top 10 vulnerabilities
- Secure coding violations
- Authentication weaknesses
- Injection vulnerabilities


### 🤖 AI-Powered Recommendations

The platform provides:

- Vulnerability explanations
- Severity classification
- Secure coding recommendations
- Corrected code examples
- Pull Request style summaries


The project combines:


- Artificial Intelligence
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Static Code Analysis
- OWASP Secure Coding Standards


to help developers identify and fix issues earlier in the software development lifecycle.



---

# 🎯 Problem Statement


Modern software applications are released frequently, making manual security reviews difficult and expensive.


Developers may introduce:

- SQL Injection vulnerabilities
- Hardcoded credentials
- Unsafe command execution
- Weak authentication mechanisms
- Poor coding practices


These issues are often discovered late during:

- Testing phase
- Production deployment
- Security audits


The objective of this project is to build an AI-powered code review assistant that automatically analyzes source code and provides actionable feedback before deployment.



---

# 🎯 Project Objectives


The main objectives of this project are:


## 1. Automated Code Review

Develop an AI-based platform that automatically reviews source code for:

- Code quality issues
- Security vulnerabilities
- Best practice violations


---


## 2. Security Vulnerability Detection

Detect OWASP-based security issues including:


- SQL Injection
- Command Injection
- Hardcoded Secrets
- Cross-Site Scripting
- Insecure Deserialization
- Weak Authentication
- Broken Access Control


---


## 3. AI-Based Remediation

Generate:


- Fix recommendations
- Secure coding explanations
- Corrected code examples


based on industry security standards.



---


## 4. RAG-Based Secure Coding Assistant


Provide developers with an intelligent assistant that can:


- Explain vulnerabilities
- Answer security questions
- Retrieve OWASP guidance
- Provide secure alternatives


using a secure coding knowledge base.



---


## 5. Automated Review Reports


Generate professional review reports containing:


- Code analysis summary
- Security findings
- Severity classification
- Recommended fixes
- Code improvement suggestions



---

# ✨ Key Features


# 📂 1. Code Submission Module


The system supports multiple ways to submit source code:


### File Upload

Supported:

- Python files (`.py`)
- Java files (`.java`)



### Direct Code Input

Developers can paste source code directly into the application.



Features:

✅ Automatic language detection

✅ File processing

✅ Source code extraction

✅ Review initiation



---


# 🌐 2. Automatic Language Detection


The application automatically identifies:


Supported languages:


🐍 Python

☕

Java



The detected language determines the appropriate analysis pipeline.



---

# ✅ 3. Syntax Validation


Before security analysis, the system validates source code syntax.



## Python Syntax Validation


Uses:

- Python AST Parser


Provides:

- Syntax checking
- Error location
- Validation messages



---


## Java Syntax Validation


Uses:

- Java Parser (`javalang`)
- Java compilation validation


Provides:

- Syntax checking
- Parsing errors
- Compilation feedback



---


# 🔍 4. Code Quality Analysis


The Code Analysis Agent identifies:


- Unused variables
- Unused imports
- Long methods
- Long lines
- Magic numbers
- Duplicate imports
- Deep nesting
- Poor exception handling
- Console logging
- Infinite loops
- Maintainability issues



---

# 🔒 5. Security Vulnerability Detection


The Security Analysis Agent detects OWASP-based vulnerabilities:


| Vulnerability | Severity |
|---|---|
| SQL Injection | High |
| Command Injection | Critical |
| Hardcoded Secrets | High |
| Insecure Deserialization | High |
| Weak Authentication | High |
| Cross-Site Scripting (XSS) | Medium |
| Path Traversal | High |
| Weak Cryptography | Medium |
| Weak Random Generation | Medium |



Each vulnerability report contains:


- Vulnerability name
- Severity level
- Risk explanation
- Recommended fix
- Secure coding practice



---

# 🔧 6. AI Remediation Suggestions


The Remediation Agent generates:


- Security fixes
- Refactoring suggestions
- Secure coding alternatives
- Corrected code examples



Example:


Before:


```java
statement.executeQuery(
"SELECT * FROM users WHERE id=" + id
);
# 🤖 Multi-Agent Architecture


The AI Code Review & Security Analysis Agent follows a modular multi-agent architecture where each agent performs a specific responsibility in the software review lifecycle.


The system consists of:


1. Code Analysis Agent
2. Security Vulnerability Agent
3. Remediation Agent
4. PR Summary Agent
5. Conversational Code Assistant
6. Orchestrator Agent



---

# 🧠 Agent Responsibilities


# 1. 🔍 Code Analysis Agent


## Purpose

The Code Analysis Agent analyzes source code quality and identifies maintainability issues, code smells, and programming best-practice violations.



## Responsibilities


- Analyze code structure
- Detect poor coding practices
- Identify maintainability issues
- Find code smells
- Generate quality recommendations



## Detects


### Code Smells

- Long methods
- Long lines
- Deep nesting
- Duplicate code patterns
- Too many parameters


### Maintainability Issues

- Unused variables
- Unused imports
- Global variables
- Magic numbers
- Poor exception handling
- Empty exception blocks


### Programming Issues

- Infinite loops
- Console logging
- Generic exception handling
- TODO/FIXME comments



## Output Example


```json
{
 "issue": "Unused Variable",
 "severity": "Medium",
 "description": "Unused variables reduce code readability",
 "recommendation": "Remove unused variables"
}
# 🔒 Security Testing & Validation


The AI Code Review & Security Analysis Agent was tested using intentionally vulnerable Python and Java source code samples.


The purpose of testing was to validate:


- Vulnerability detection accuracy
- Severity classification
- Security recommendations
- AI remediation quality
- OWASP compliance


Testing was performed against common security vulnerabilities from the OWASP Top 10.



---

# 📊 Security Testing Results


| Vulnerability | Status | Severity |
|---|---|---|
| SQL Injection | ✅ Tested | High |
| Hardcoded Secrets | ✅ Tested | High |
| Command Injection | ✅ Tested | Critical |
| Insecure Deserialization | ✅ Tested | High |
| Weak Authentication | ✅ Tested | High |
| Cross-Site Scripting (XSS) | ⚠️ Validation Pending | Medium |
| Broken Access Control | ⚠️ Validation Pending | High |



---

# 🧪 Vulnerability Test Cases


The following test cases were created using vulnerable source code examples.



---

# 1. SQL Injection Test


## Objective


Verify whether the Security Agent detects unsafe SQL query construction.



## Vulnerable Code


```java
String query =
"SELECT * FROM users WHERE id="
+ userInput;


Statement stmt =
connection.createStatement();

ResultSet rs =
stmt.executeQuery(query);
# 🛠 Technology Stack


The AI Code Review & Security Analysis Agent is built using modern Artificial Intelligence, software engineering, and security technologies.



---

# 💻 Programming Languages


## Python


Used for:


- AI agent implementation
- Backend processing
- RAG pipeline
- Security analysis
- Streamlit application



## Java


Supported for:


- Source code analysis
- Syntax validation
- Security vulnerability detection
- Code quality analysis



---

# 🎨 Frontend Technology


## Streamlit


Streamlit is used to build the interactive user interface.



Features:


- Source code upload
- Code editor
- Analysis dashboard
- Security reports
- PDF download
- AI assistant interface



---

# ⚙ Backend Technology


## Python Backend


Responsible for:


- File processing
- Language detection
- Syntax validation
- Agent execution
- Report generation
- RAG integration



---

# 🤖 Artificial Intelligence Technologies


## LangChain


Used for:


- LLM integration
- Prompt management
- RAG workflow
- Document retrieval



---

## LangGraph


Used for:


- Multi-agent workflow management
- Agent communication
- State management
- Sequential execution



---

## Groq LLM


Used for:


- AI reasoning
- Security explanation generation
- Code remediation
- Pull request summaries



---

# 🧠 Embedding Model


## HuggingFace Sentence Transformers


Model:


```text
sentence-transformers/all-MiniLM-L6-v2
# 🚀 Deployment Guide


The AI Code Review & Security Analysis Agent can be deployed locally or on cloud platforms.



---

# 🌐 Streamlit Cloud Deployment


The application supports deployment using Streamlit Cloud.



## Deployment Steps


### Step 1

Push the project repository to GitHub.



### Step 2

Open Streamlit Cloud:



```text
https://streamlit.io/cloud