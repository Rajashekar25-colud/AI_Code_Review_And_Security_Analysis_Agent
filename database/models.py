"""
Table definitions and schema creation.

Call create_tables() once at app startup (app.py does this via
database/migrations.py) - CREATE TABLE IF NOT EXISTS is safe to
run on every launch.
"""

from database.connection import get_connection


def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )

    # Backfill "name" column for databases created before this
    # field existed - SQLite allows adding a nullable column
    # after the fact.
    try:
        cur.execute("ALTER TABLE users ADD COLUMN name TEXT")
    except Exception:
        pass

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id                     INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id                INTEGER NOT NULL,
            filename               TEXT,
            language               TEXT,
            overall_score          INTEGER,
            security_score         INTEGER,
            quality_score          INTEGER,
            maintainability_score  INTEGER,
            reliability_score      INTEGER,
            findings_json          TEXT,
            summary                TEXT,
            created_at             TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id   INTEGER NOT NULL,
            role        TEXT NOT NULL,
            message     TEXT NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (review_id) REFERENCES reviews (id) ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            token       TEXT PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            expires_at  TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()