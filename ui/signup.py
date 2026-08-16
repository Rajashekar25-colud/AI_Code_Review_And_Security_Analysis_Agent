import streamlit as st

from database.auth import create_user


def render_signup_page():
    """
    Signup form. On success, drops the person back to the login
    page (st.session_state.auth_page = "login") rather than
    logging them in automatically, so they confirm their
    credentials work end-to-end.
    """

    st.title("🤖 Smart Code Inspection Platform")
    st.subheader("Create Account")

    with st.form("signup_form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Sign Up", width="stretch")

    if submitted:

        if not name or not email or not password or not confirm:
            st.error("Fill in all fields.")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        success, message = create_user(email, password, name)

        if not success:
            st.error(message)
            return

        st.success(message + " Please log in.")
        st.session_state.auth_page = "login"

    st.divider()

    st.caption("Already have an account?")

    if st.button("Log in instead", width="stretch"):
        st.session_state.auth_page = "login"
        st.rerun()