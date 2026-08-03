import streamlit as st


def render_assistant_page(review_result=None):
    """
    RAG Powered AI Security Assistant
    """

    st.title("🤖 AI Security Assistant")

    st.markdown("""
Ask anything about:

- OWASP Top 10
- Secure Coding
- Python Security
- Java Security
- Code Review
- Vulnerability Remediation
""")

    if "assistant" not in st.session_state:
        st.session_state.assistant = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.chat_input(
        "Ask a security question..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Thinking..."):

            try:

                if st.session_state.assistant is None:

                    from agents.conversational_assistant import (
                        ConversationalAssistant
                    )

                    st.session_state.assistant = (
                        ConversationalAssistant()
                    )

                response = (
                    st.session_state.assistant.ask(question)
                )

                answer = response.get(
                    "answer",
                    "No response generated."
                )

                sources = response.get(
                    "sources",
                    []
                )

            except Exception as e:

                answer = f"❌ {str(e)}"
                sources = []

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer,
                "sources": sources
            }
        )

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):

            st.write(chat["answer"])

            if chat.get("sources"):

                st.caption("Sources")

                for source in chat["sources"]:
                    st.write(f"• {source}")

    if review_result:

        st.divider()

        st.subheader("Latest Review Summary")

        findings = review_result.get(
            "findings",
            []
        )

        st.metric(
            "Issues Found",
            len(findings)
        )

        summary = review_result.get(
            "pr_summary",
            ""
        )

        if summary:

            st.markdown(summary)