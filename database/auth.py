"""
Password hashing, user authentication, and persistent login
sessions.

Uses PBKDF2-HMAC-SHA256 (stdlib hashlib) for passwords and
secrets.token_urlsafe (stdlib secrets) for session tokens - no
extra dependency needed.
"""

import hashlib
import secrets
from datetime import datetime, timedelta

from database.connection import get_connection

ITERATIONS = 200_000
SESSION_LIFETIME_DAYS = 7


def _hash_password(password: str, salt: str = None):

    if salt is None:
        salt = secrets.token_hex(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        ITERATIONS
    ).hex()

    return f"{salt}${digest}"


def _verify_password(password: str, stored_hash: str) -> bool:

    try:
        salt, _ = stored_hash.split("$", 1)
    except ValueError:
        return False

    return secrets.compare_digest(
        _hash_password(password, salt),
        stored_hash
    )


def create_user(email: str, password: str, name: str = ""):
    """
    Registers a new user. Returns (success: bool, message: str).
    """

    email = email.strip().lower()
    name = name.strip()

    if not email or "@" not in email:
        return False, "Enter a valid email address."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if not name:
        return False, "Enter your name."

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = ?", (email,))

    if cur.fetchone():
        conn.close()
        return False, "An account with this email already exists."

    password_hash = _hash_password(password)

    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )

    conn.commit()
    conn.close()

    return True, "Account created successfully."


def authenticate_user(email: str, password: str):
    """
    Verifies credentials. Returns (user_dict_or_None, message: str).
    """

    email = email.strip().lower()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = ?",
        (email,)
    )

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None, "No account found with this email."

    if not _verify_password(password, row["password_hash"]):
        return None, "Incorrect password."

    return (
        {
            "id": row["id"],
            "name": row["name"] or row["email"].split("@")[0],
            "email": row["email"]
        },
        "Login successful."
    )


def create_session(user_id: int) -> str:
    """
    Creates a persistent login session for a user and returns the
    token. The token is meant to be stored in the URL query params
    (see app.py) so login survives a page refresh.
    """

    token = secrets.token_urlsafe(32)
    expires_at = (
        datetime.utcnow() + timedelta(days=SESSION_LIFETIME_DAYS)
    ).isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, user_id, expires_at)
    )

    conn.commit()
    conn.close()

    return token


def get_user_by_session(token: str):
    """
    Returns the user dict for a valid, non-expired session token,
    or None if the token is missing, invalid, or expired.
    """

    if not token:
        return None

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sessions.user_id, sessions.expires_at,
               users.name, users.email
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.token = ?
        """,
        (token,)
    )

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    expires_at = datetime.fromisoformat(row["expires_at"])

    if expires_at < datetime.utcnow():
        delete_session(token)
        return None

    return {
        "id": row["user_id"],
        "name": row["name"] or row["email"].split("@")[0],
        "email": row["email"]
    }


def delete_session(token: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM sessions WHERE token = ?", (token,))

    conn.commit()
    conn.close()