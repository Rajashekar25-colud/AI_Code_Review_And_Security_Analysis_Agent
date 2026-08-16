import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def get_groq_model(
    temperature: float = 0.2,
    max_tokens: int = 1024
):
    """
    Returns a configured ChatGroq client.

    max_tokens controls how much output the model is allowed to
    generate in one response. Callers that need longer, structured
    output (JSON findings arrays, detailed remediation reports)
    should pass a higher value explicitly - the previous fixed
    512-token default was silently truncating responses mid-string
    for anything beyond a couple of short findings, which is what
    caused "Unterminated string" JSON parse failures in
    agents/java_security_analyzer.py and cut-off remediation
    reports.
    """

    api_key = os.getenv(
        "GROQ_API_KEY"
    )


    if not api_key:

        raise ValueError(
            "GROQ_API_KEY is not configured."
        )


    model = os.getenv(
        "GROQ_MODEL"
    )


    if not model:

        raise ValueError(
            "GROQ_MODEL is not configured."
        )


    return ChatGroq(

        groq_api_key=api_key,

        model=model,

        temperature=temperature,

        max_tokens=max_tokens

    )