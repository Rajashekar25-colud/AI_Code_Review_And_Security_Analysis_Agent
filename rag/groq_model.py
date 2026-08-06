import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def get_groq_model(
    temperature: float = 0.2
):

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

        max_tokens=512

    )