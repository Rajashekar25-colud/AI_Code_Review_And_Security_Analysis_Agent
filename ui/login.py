import streamlit as st

from database.auth import authenticate_user, create_session


def render_login_page():
    """
    Login form. On success, sets st.session_state.user, creates a
    persistent session token, and stores it in the URL query
    params so the login survives a page refresh.
    """

    st.title("🤖 Smart Code Inspection Platform")
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

        token = create_session(user["id"])

        st.session_state.user = user
        st.query_params["session"] = token

        st.rerun()

    st.divider()

    st.caption("Don't have an account?")

    if st.button("Create one", width="stretch"):
        st.session_state.auth_page = "signup"
        st.rerun()