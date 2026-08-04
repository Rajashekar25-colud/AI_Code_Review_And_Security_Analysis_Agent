import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


# Default model for project usage
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"


def get_groq_model(
    temperature: float = 0.2
):
    """
    Returns configured Groq LLM instance.

    Environment variables:

    GROQ_API_KEY  -> Required
    GROQ_MODEL    -> Optional

    Example:

    GROQ_MODEL=llama-3.3-70b-versatile
    """

    api_key = os.getenv(
        "GROQ_API_KEY"
    )


    if not api_key:

        raise ValueError(
            "GROQ_API_KEY is not configured."
        )


    model = os.getenv(
        "GROQ_MODEL",
        DEFAULT_GROQ_MODEL
    )


    return ChatGroq(

        groq_api_key=api_key,

        model=model,

        temperature=temperature

    )