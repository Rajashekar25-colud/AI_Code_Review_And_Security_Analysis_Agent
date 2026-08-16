"""
CRUD helpers for reviews and chat messages.

Scores are computed via modules/score_calculator.py, so every
caller (dashboard, history, PDF export) reads the same numbers
instead of recomputing them differently in each page.
"""

import json

from database.connection import get_connection
from modules.score_calculator import calculate_score


def compute_scores(findings: list) -> dict:
    """
    Turns a findings list into a 0-100 score per dimension.
    """

    overall = calculate_score(findings)

    return {
        "overall_score": overall,
        "security_score": overall,
        "quality_score": overall,
        "maintainability_score": overall,
        "reliability_score": overall
    }


def save_review(
    user_id: int,
    filename: str,
    language: str,
    findings: list,
    summary: str
) -> int:
    """
    Persists a completed review. Returns the new review's id.
    """

    scores = compute_scores(findings)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO reviews (
            user_id, filename, language,
            overall_score, security_score, quality_score,
            maintainability_score, reliability_score,
            findings_json, summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            filename,
            language,
            scores["overall_score"],
            scores["security_score"],
            scores["quality_score"],
            scores["maintainability_score"],
            scores["reliability_score"],
            json.dumps(findings),
            summary
        )
    )

    review_id = cur.lastrowid

    conn.commit()
    conn.close()

    return review_id


def get_history(user_id: int) -> list:
    """
    Returns all reviews for a user, most recent first, with
    findings_json decoded back into a list.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM reviews
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()

    for row in rows:
        row["findings"] = json.loads(row["findings_json"] or "[]")

    return rows


def get_review_by_id(review_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    result = dict(row)
    result["findings"] = json.loads(result["findings_json"] or "[]")

    return result


def delete_review(review_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM reviews WHERE id = ?", (review_id,))

    conn.commit()
    conn.close()


def save_chat_message(review_id: int, role: str, message: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat_messages (review_id, role, message) VALUES (?, ?, ?)",
        (review_id, role, message)
    )

    conn.commit()
    conn.close()


def get_chat_history(review_id: int) -> list:

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, message, created_at FROM chat_messages
        WHERE review_id = ?
        ORDER BY created_at ASC
        """,
        (review_id,)
    )

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()

    return rows


def delete_chat_history(review_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM chat_messages WHERE review_id = ?", (review_id,))

    conn.commit()
    conn.close()