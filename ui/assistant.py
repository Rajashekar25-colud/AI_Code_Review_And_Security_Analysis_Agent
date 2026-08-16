import streamlit as st

from database.repository import save_chat_message, get_chat_history, delete_chat_history


def get_review_key(review_result):
    """
    A stable-ish key that scopes chat history to a specific
    review, so switching between past/new reviews doesn't mix
    up conversations. Falls back to a shared "general" thread
    when there is no active review.
    """

    if not review_result:
        return "general"

    filename = review_result.get("filename") or review_result.get("file_name")
    findings_count = len(review_result.get("findings", []))

    if filename:
        return f"{filename}:{findings_count}"

    return f"review:{id(review_result)}"


def render_assistant_page(review_result=None):
    """
    Embedded, ChatGPT-style follow-up chat, shown directly under a
    completed review (called from ui/review_page.py - there is no
    separate "AI Assistant" nav page).

    - Multi-turn: follow-up questions ("fix that", "explain more")
      resolve against the conversation so far.
    - Scoped: grounded on the current review's findings plus the
      OWASP/secure coding knowledge base.
    - Persistent per review: when the review is saved in the
      database (st.session_state.active_review_id is set), turns
      are also persisted so they survive logout/restore.
    """

    st.subheader("🤖 Ask about this review")

    st.caption(
        "Ask follow-up questions about the findings above, or "
        "about secure coding and OWASP best practices in general."
    )

    if "assistant" not in st.session_state:
        st.session_state.assistant = None

    if "chat_threads" not in st.session_state:
        st.session_state.chat_threads = {}

    active_review_id = st.session_state.get("active_review_id")
    thread_key = get_review_key(review_result)

    # ------------------------------------------------------
    # Hydrate thread from the database the first time this
    # review is opened in this session (e.g. after Restore
    # from History, or a fresh login).
    # ------------------------------------------------------

    if thread_key not in st.session_state.chat_threads:

        thread = []

        if active_review_id:

            db_messages = get_chat_history(active_review_id)

            pending_question = None

            for row in db_messages:

                if row["role"] == "user":
                    pending_question = row["message"]

                elif row["role"] == "assistant" and pending_question is not None:
                    thread.append(
                        {
                            "question": pending_question,
                            "answer": row["message"],
                            "sources": []
                        }
                    )
                    pending_question = None

        st.session_state.chat_threads[thread_key] = thread

    thread = st.session_state.chat_threads[thread_key]

    # ------------------------------------------------------
    # Render existing conversation for this thread
    # ------------------------------------------------------

    for turn in thread:

        with st.chat_message("user"):
            st.write(turn["question"])

        with st.chat_message("assistant"):

            st.write(turn["answer"])

            if turn.get("sources"):

                with st.expander("Sources"):
                    for source in turn["sources"]:
                        st.write(f"• {source}")

    # ------------------------------------------------------
    # New message
    # ------------------------------------------------------

    question = st.chat_input("Ask a follow-up question...")

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    if st.session_state.assistant is None:

                        from agents.conversational_assistant import (
                            ConversationalAssistant
                        )

                        st.session_state.assistant = (
                            ConversationalAssistant()
                        )

                    findings = (
                        review_result.get("findings", [])
                        if review_result else []
                    )

                    response = st.session_state.assistant.ask(
                        question,
                        chat_history=thread,
                        review_findings=findings
                    )

                    answer = response.get(
                        "answer", "No response generated."
                    )
                    sources = response.get("sources", [])

                except Exception as e:

                    answer = f"❌ {str(e)}"
                    sources = []

            st.write(answer)

            if sources:

                with st.expander("Sources"):
                    for source in sources:
                        st.write(f"• {source}")

        thread.append(
            {
                "question": question,
                "answer": answer,
                "sources": sources
            }
        )

        if active_review_id:

            save_chat_message(active_review_id, "user", question)
            save_chat_message(active_review_id, "assistant", answer)

    if thread:

        if st.button("🗑 Clear conversation", width="content"):

            st.session_state.chat_threads[thread_key] = []

            if active_review_id:
                delete_chat_history(active_review_id)

            st.rerun()