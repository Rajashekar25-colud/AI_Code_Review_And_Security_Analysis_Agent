"""
SQLite connection layer.

Creates (if missing) a local SQLite database file at the project
root and exposes a single get_connection() helper used by every
other module in database/.
"""

import os
import sqlite3
from contextlib import contextmanager

from config import DATABASE_PATH as DB_PATH


def get_connection():
    """
    Returns a new sqlite3 connection with foreign keys enabled
    and row access by column name.
    """

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


@contextmanager
def get_cursor(commit=False):
    """
    Context manager for a cursor that auto-closes the connection.

    Usage:
        with get_cursor(commit=True) as cur:
            cur.execute("INSERT INTO ...", (...))
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        yield cur

        if commit:
            conn.commit()

    finally:
        conn.close()