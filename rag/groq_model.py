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
    generate in one response - callers needing longer, structured
    output (JSON findings arrays, detailed remediation reports)
    should pass a higher value explicitly.

    timeout/max_retries are set generously because longer
    generations (higher max_tokens) take longer to complete, and
    ChatGroq's short default timeout was causing "Connection
    error" failures specifically on the longer remediation/PR
    summary prompts, even though short test prompts worked fine -
    the connection itself was never the problem, the response
    just wasn't finishing before the old default timeout hit.
    max_retries adds automatic retry on transient network blips
    instead of failing immediately on the first hiccup.
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

        max_tokens=max_tokens,

        timeout=90,

        max_retries=2

    )