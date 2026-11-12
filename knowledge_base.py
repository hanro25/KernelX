
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "sysmedic_knowledge.db"


def initialise_database():
    """Create the local SysMedic knowledge base."""

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS troubleshooting_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                symptoms TEXT NOT NULL,
                root_cause TEXT NOT NULL,
                resolution TEXT NOT NULL,
                successful INTEGER NOT NULL DEFAULT 0,
                approved_for_reuse INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_case_category
            ON troubleshooting_cases(category)
        """)


def save_case(
    category,
    symptoms,
    root_cause,
    resolution,
    successful,
    approved_for_reuse=False
):
    """Save a reviewed troubleshooting case."""

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            INSERT INTO troubleshooting_cases (
                category,
                symptoms,
                root_cause,
                resolution,
                successful,
                approved_for_reuse,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            category,
            symptoms,
            root_cause,
            resolution,
            int(successful),
            int(approved_for_reuse),
            datetime.now(timezone.utc).isoformat()
        ))


def get_approved_cases(category=None):
    """Retrieve approved cases for future recommendations."""

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        if category:
            rows = connection.execute("""
                SELECT * FROM troubleshooting_cases
                WHERE approved_for_reuse = 1
                AND category = ?
                ORDER BY created_at DESC
            """, (category,)).fetchall()
        else:
            rows = connection.execute("""
                SELECT * FROM troubleshooting_cases
                WHERE approved_for_reuse = 1
                ORDER BY created_at DESC
            """).fetchall()

        return [dict(row) for row in rows]
