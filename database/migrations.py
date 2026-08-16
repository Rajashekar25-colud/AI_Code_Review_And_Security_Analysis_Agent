"""
Startup migration runner.

Import and call run_migrations() once, early in app.py — before
any page tries to read/write the database. Safe to call on every
launch since create_tables() uses CREATE TABLE IF NOT EXISTS.
"""

from database.models import create_tables


def run_migrations():
    create_tables()