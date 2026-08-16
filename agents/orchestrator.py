from typing import TypedDict
from concurrent.futures import ThreadPoolExecutor

from langgraph.graph import StateGraph, END

from agents.code_analysis_agent import CodeAnalysisAgent
from agents.security_agent import SecurityAgent
from agents.remediation_agent import RemediationAgent
from agents.pr_summary_agent import PRSummaryAgent

from modules.java_compiler import JavaCompiler
from modules.severity import normalize_findings
import logging

logger = logging.getLogger(__name__)


class ReviewState(TypedDict):
    source_code: str
    language: str
    code_findings: list
    security_findings: list
    findings: list
    remediation: dict
    pr_summary: str


class Orchestrator:

    def __init__(self):

        self.code_agent = CodeAnalysisAgent()
        self.security_agent = SecurityAgent()
        self.remediation_agent = RemediationAgent()
        self.summary_agent = PRSummaryAgent()

        # Java compiler (safe for Streamlit Cloud)
        self.java_compiler = JavaCompiler()

        builder = StateGraph(ReviewState)

        builder.add_node(
            "parallel_analysis",
            self.parallel_analysis
        )

        builder.add_node(
            "merge",
            self.merge_findings
        )

        builder.add_node(
            "remediation",
            self.remediation
        )

        builder.add_node(
            "summary",
            self.summary
        )

        builder.set_entry_point(
            "parallel_analysis"
        )

        builder.add_edge(
            "parallel_analysis",
            "merge"
        )

        builder.add_edge(
            "merge",
            "remediation"
        )

        builder.add_edge(
            "remediation",
            "summary"
        )

        builder.add_edge(
            "summary",
            END
        )

        self.graph = builder.compile()

    ##################################################
    # Parallel Analysis
    ##################################################

    def parallel_analysis(self, state):

        class_directory = None

        if state["language"] == "Java":

            try:

                compile_result = self.java_compiler.compile(
                    state["source_code"]
                )

                if compile_result.get("success"):
                    class_directory = compile_result.get("class_dir")
                else:
                    logger.info(
                        "Java compilation skipped: %s",
                        compile_result.get("message")
                    )

            except Exception as e:

                logger.info("Java compilation unavailable: %s", str(e))

                class_directory = None

        with ThreadPoolExecutor(max_workers=2) as executor:

            code_future = executor.submit(
                self.code_agent.analyze,
                state["source_code"],
                state["language"]
            )

            security_future = executor.submit(
                self.security_agent.analyze,
                state["source_code"],
                state["language"],
                class_directory
            )

            code_result = code_future.result()
            security_result = security_future.result()

        state["code_findings"] = code_result.get(
            "findings",
            []
        )

        state["security_findings"] = security_result.get(
            "findings",
            []
        )

        return state

    ##################################################
    # Merge Findings
    #
    # Each tool runner tags its own "agent" field on every
    # finding it produces. Some producers (e.g. the Groq-based
    # Java security analyzer) don't set one, so we default it
    # here based on which pipeline stage the finding came from -
    # setdefault() never overwrites a value a tool already set.
    ##################################################

    def merge_findings(self, state):

        code_findings = state.get("code_findings", [])
        security_findings = state.get("security_findings", [])

        for finding in code_findings:
            finding.setdefault("agent", "Code Analysis Agent")

        for finding in security_findings:
            finding.setdefault("agent", "Security Vulnerability Agent")

        findings = code_findings + security_findings

        state["findings"] = normalize_findings(findings)

        return state

    ##################################################
    # Remediation
    ##################################################

    def remediation(self, state):

        result = self.remediation_agent.generate(
            findings=state["findings"],
            source_code=state["source_code"],
            language=state["language"]
        )

        state["remediation"] = result

        return state

    ##################################################
    # PR Summary
    ##################################################

    def summary(self, state):

        result = self.summary_agent.generate_summary(
            source_code=state["source_code"],
            language=state["language"],
            findings=state["findings"],
            remediation=state["remediation"]
        )

        state["pr_summary"] = result.get(
            "summary",
            ""
        )

        return state

    ##################################################
    # Execute Workflow
    ##################################################

    def analyze_code(
        self,
        source_code,
        language
    ):

        state = {
            "source_code": source_code,
            "language": language,
            "code_findings": [],
            "security_findings": [],
            "findings": [],
            "remediation": {},
            "pr_summary": ""
        }

        return self.graph.invoke(state)