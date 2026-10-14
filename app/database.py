
import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "lld_practice.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                problem_title TEXT NOT NULL,
                submission TEXT NOT NULL,
                score INTEGER NOT NULL,
                feedback TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_attempt(problem, design, evaluation):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO attempts (
                problem_id, problem_title, submission, score, feedback
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            problem["id"],
            problem["title"],
            json.dumps(design),
            evaluation["score"],
            json.dumps(evaluation["feedback"])
        ))
        return cursor.lastrowid


def get_attempts():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM attempts ORDER BY id DESC"
        ).fetchall()

        attempts = []
        for row in rows:
            item = dict(row)
            item["submission"] = json.loads(item["submission"])
            item["feedback"] = json.loads(item["feedback"])
            attempts.append(item)

        return attempts
