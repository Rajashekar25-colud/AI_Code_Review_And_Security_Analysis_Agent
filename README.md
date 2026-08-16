# Development of Smart Code Inspection Platform with Vulnerability Detection System

*(Group 1 — formerly titled "AI Code Review & Security Analysis Agent")*

A multi-agent platform that automatically analyzes Python and Java source code for code quality issues, OWASP-standard security vulnerabilities, and best-practice violations — producing severity-scored findings, AI-generated remediation, a PR-style summary, and an exportable PDF report, plus a RAG-grounded conversational assistant for follow-up questions.

---

## 1. Problem Statement

Manual code review is slow, subjective, and doesn't scale with growing codebases. Developers often lack immediate access to expert guidance on secure coding practices during active development, leaving vulnerabilities and quality issues undetected until late in the development lifecycle. This project addresses that gap with an automated, explainable, multi-agent review pipeline.

---

## 2. Architecture

```
                    Source Code (paste or upload)
                              |
                              v
                    Language Detection
                              |
                              v
                    Syntax Validation
                              |
                              v
                    Orchestrator (LangGraph)
              ┌───────────────┴───────────────┐
              v                                v
     Code Analysis Agent            Security Vulnerability Agent
     (Pylint, Radon, PMD,           (Bandit, custom Python rules,
      Checkstyle, custom            SpotBugs, Groq LLM for Java)
      Java analyzer)
              └───────────────┬───────────────┘
                              v
                    Severity Normalization
                    (config-driven, per-tool)
                              |
                              v
                    OWASP Category Tagging
                              |
                              v
                    Remediation Agent (Groq LLM)
                              |
                              v
                    PR Summary Agent (Groq LLM)
                              |
                              v
        Dashboard  +  PDF Report  +  Embedded Chat Assistant
```

### Multi-agent pipeline

The **Code Analysis Agent** and **Security Vulnerability Agent** run **in parallel** (via `ThreadPoolExecutor`), each wrapping several underlying static analysis tools plus, for Java security findings, a Groq LLM pass grounded in the same rules the platform documents. Their outputs are merged into one findings list before moving downstream.

| Agent | Responsibility | Tools used |
|---|---|---|
| Code Analysis Agent | Code smells, complexity, design anti-patterns | Pylint, Radon (Python); PMD, Checkstyle, custom analyzer (Java) |
| Security Vulnerability Agent | OWASP-standard vulnerabilities | Bandit + custom rule set (Python); SpotBugs + Groq LLM (Java) |
| Remediation Agent | Fix recommendations with corrected code examples | Groq LLM |
| PR Summary Agent | Executive summary, severity breakdown, prioritized fix list | Groq LLM |
| Conversational Code Assistant | RAG-grounded Q&A on findings and secure coding practices | Groq LLM + Chroma vector store |

### Severity normalization — no hardcoded business logic

Every underlying tool reports severity differently (Bandit: LOW/MEDIUM/HIGH; PMD: priority 1–5; SpotBugs: priority 1–3; Pylint: convention/refactor/warning/error/fatal; Radon: complexity rank A–F). Rather than hand-coding `if/elif` severity logic per tool, every mapping lives in an editable JSON config file under `config/`, loaded at runtime:

- `config/severity_map.json` — keyword→severity fallback for tools with no native severity
- `config/severity_weights.json` — severity→score-penalty weights (single source of truth, used identically by the database and the dashboard)
- `config/owasp_map.json` — keyword→OWASP Top 10 (2021) category
- `config/pmd_priority_map.json`, `config/spotbugs_priority_map.json`, `config/pylint_severity_map.json`, `config/radon_severity_map.json`, `config/java_quality_severity.json` — per-tool native-scale translation
- `config/risk_thresholds.json` — score→risk-band labels (Excellent/Good/Moderate/Poor/Critical)

`modules/severity.py` is the single module responsible for reading these files and normalizing every finding's `severity`, `type`, `description`, `recommendation`, and `owasp_category` fields before they reach the dashboard, chat, database, or PDF report — guaranteeing every downstream consumer sees identical, consistent data regardless of which tool produced a given finding.

---

## 3. Modules

1. **Code Submission** (`ui/review_page.py`) — paste or upload `.py`/`.java` files, with syntax validation before analysis begins.
2. **Secure Coding Knowledge Base & RAG Pipeline** (`rag/`) — OWASP guidelines and secure coding documents chunked, embedded, and indexed into a Chroma vector store; retrieved via MMR search for grounded chat answers.
3. **Multi-Agent Orchestration** (`agents/orchestrator.py`) — LangGraph state machine coordinating parallel analysis, merge, remediation, and summary stages.
4. **Findings Display & Severity Scoring** (`ui/dashboard.py`) — severity counts, health score gauge, radar chart (Security/Quality/Maintainability/Reliability/Complexity), OWASP coverage.
5. **Conversational Assistant** (`ui/assistant.py`, `agents/conversational_assistant.py`) — embedded directly under each review's results, multi-turn, grounded on both the knowledge base and the current review's findings, persisted per review in the database.
6. **Report Generation & Export** (`modules/report_generator.py`, `ui/report_page.py`) — exportable PDF with findings summary, severity breakdown, and remediation roadmap.

---

## 4. Data Model

```
Users            Reviews                    ChatMessages       Sessions
-----            -------                    ------------       --------
id               id                         id                 token (PK)
name             user_id (FK)               review_id (FK)     user_id (FK)
email            filename                   role               created_at
password_hash    language                   message            expires_at
created_at       overall_score              created_at
                 security_score
                 quality_score
                 maintainability_score
                 reliability_score
                 findings_json
                 summary
                 created_at
```

Passwords are hashed with PBKDF2-HMAC-SHA256 (stdlib `hashlib`, 200,000 iterations, unique salt per user). Login sessions use a random token (`secrets.token_urlsafe`) stored in the URL query string, so login survives a page refresh without a third-party auth library.

---

## 5. Tech Stack

- **UI**: Streamlit
- **Orchestration**: LangGraph
- **LLM**: Groq (Llama models) via `langchain-groq`
- **RAG**: `langchain`, Chroma vector store, HuggingFace sentence-transformers embeddings
- **Static analysis**: Pylint, Radon, Bandit (Python); PMD, Checkstyle, SpotBugs (Java)
- **Database**: SQLite (stdlib `sqlite3`)
- **Reporting**: ReportLab (PDF)
- **Testing**: pytest

---

## 6. Running the Project

```powershell
# 1. Create and activate a virtual environment (Python 3.11 or 3.12 — see Known Limitations)
py -3.11 -m venv venv
.\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env
# then set GROQ_API_KEY in .env

# 4. Build the knowledge base (first run only, or after clearing chroma_db/)
python rag/build_knowledgebase.py

# 5. Run the tests
python -m pytest tests/ -v

# 6. Launch the app
python -m streamlit run app.py
```

---

## 7. Testing

- `tests/test_severity.py` — unit tests for severity normalization, OWASP tagging, and score calculation. No external dependencies; runs anywhere.
- `tests/test_pipeline.py` — end-to-end integration tests running real source code through the full orchestrator. Requires `GROQ_API_KEY`; auto-skips otherwise.

Manual end-to-end validation has been performed across multiple distinct Python and Java samples covering SQL Injection, Command Injection, Path Traversal, Insecure Deserialization, Hardcoded Secrets, and Weak Cryptography, exceeding the minimum 3-sample demonstration requirement.

---

## 8. Known Limitations

- **Python 3.14 is not currently supported** — the LangChain/Pydantic dependency stack does not yet support Python 3.14's deferred type-annotation evaluation (PEP 649). Use Python 3.11 or 3.12.
- **Broken Access Control and Weak Authentication detection currently only covers Java** (via the Groq LLM security prompt). Python has no dedicated static rule for these two OWASP categories yet — a gap identified during evaluation against the original project spec.
- Line numbers are shown for tool-based findings (PMD, Bandit, etc.) but intentionally omitted for LLM-generated findings, since asking an LLM to determine exact source line numbers is unreliable.
- Chat history and review history are scoped per logged-in user; there is no admin/multi-tenant view.

---

## 9. Project Structure

```
AI-Code-Review-Agent/
├── app.py                  # Entry point: auth gate, routing, logging
├── config.py                # Central paths/env config
├── config/                  # Editable severity/OWASP/risk JSON mappings
├── database/                 # SQLite connection, models, auth, repository
├── agents/                    # Orchestrator + 5 agents
├── tools/                     # Static analysis tool wrappers
├── rag/                        # Knowledge base loading, embedding, vector store
├── modules/                    # Language detection, validation, scoring, PDF generation
├── ui/                          # Streamlit pages
├── knowledge_base/               # Source documents indexed into the vector store
└── tests/                         # pytest unit and integration tests
```