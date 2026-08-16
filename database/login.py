import streamlit as st

from database.auth import authenticate_user


def render_login_page():
    """
    Login form. On success, sets st.session_state.user and
    st.session_state.auth_page = None, which app.py checks to
    let the person into the main app.
    """

    st.title("🤖 AI Code Review Agent")
    st.subheader("Log In")

    with st.form("login_form"):

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Log In", width="stretch")

    if submitted:

        if not email or not password:
            st.error("Enter both email and password.")
            return

        user, message = authenticate_user(email, password)

        if user is None:
            st.error(message)
            return

        st.session_state.user = user
        st.rerun()

    st.divider()

    st.caption("Don't have an account?")

    if st.button("Create one", width="stretch"):
        st.session_state.auth_page = "signup"
        st.rerun()