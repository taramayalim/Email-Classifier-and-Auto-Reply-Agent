
import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "processed" / "email_agent.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                predicted_categories TEXT,
                priority TEXT,
                action TEXT,
                suggested_reply TEXT,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id INTEGER NOT NULL,
                feedback_type TEXT NOT NULL,
                comments TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (email_id) REFERENCES emails(id)
            )
        """)


def save_email(subject, body, categories, priority, action, reply):
    with get_connection() as connection:

        cursor = connection.execute("""
            INSERT INTO emails (
                subject, body, predicted_categories,
                priority, action, suggested_reply, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            subject,
            body,
            "; ".join(categories),
            priority,
            action,
            reply,
            datetime.now().isoformat(timespec="seconds")
        ))

        return cursor.lastrowid


def save_feedback(email_id, feedback_type, comments=""):
    if feedback_type not in ["approved", "rejected", "edited"]:
        raise ValueError("Invalid feedback type.")

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO feedback (
                email_id, feedback_type, comments, created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            email_id,
            feedback_type,
            comments,
            datetime.now().isoformat(timespec="seconds")
        ))


def get_email_history():
    with get_connection() as connection:
        return connection.execute("""
            SELECT id, subject, predicted_categories,
                   priority, action, created_at
            FROM emails ORDER BY id DESC
        """).fetchall()


def get_feedback_history():
    with get_connection() as connection:
        return connection.execute("""
            SELECT email_id, feedback_type, comments, created_at
            FROM feedback ORDER BY id DESC
        """).fetchall()
