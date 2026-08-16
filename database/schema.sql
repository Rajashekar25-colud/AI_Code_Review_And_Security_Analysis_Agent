-- AI Code Review & Security Analysis Agent
-- Database schema (SQLite)
-- Mirrors database/models.py — kept here as a standalone,
-- reviewable reference. models.py is what actually runs at
-- startup; this file is documentation/manual-setup convenience.

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

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
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id   INTEGER NOT NULL,
    role        TEXT NOT NULL,
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (review_id) REFERENCES reviews (id) ON DELETE CASCADE
);