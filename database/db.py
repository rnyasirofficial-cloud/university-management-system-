"""
Database helper module for the University Management System (UMS).
Manages SQLite connection, executes schema, seeds initial data, and provides query helpers.
"""

import sqlite3
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_DIR = Path(__file__).resolve().parent
DB_FILE = Path("/tmp/university.db") if os.getenv("VERCEL") else DB_DIR / "university.db"
SCHEMA_FILE = DB_DIR / "schema.sql"
SEED_FILE = DB_DIR / "seed.sql"


def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row factory set to dict."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_database(force_reseed: bool = False) -> None:
    """
    Initializes the database using schema.sql and seed.sql if the database
    is not created, is missing tables, or if force_reseed is True.
    """
    db_exists = DB_FILE.exists()

    conn = get_connection()
    cursor = conn.cursor()
    required_tables = {
        "Department", "Program", "Student", "Teacher", "Course",
        "Semester", "Classroom", "Course_Offering", "Enrollment",
        "Exam", "Result", "Attendance", "Timetable", "User_Account"
    }

    existing_tables = {
        row[0] for row in cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        ).fetchall()
    }

    if force_reseed:
        cursor.execute("PRAGMA foreign_keys = OFF;")
        for tbl in list(existing_tables):
            cursor.execute(f"DROP TABLE IF EXISTS \"{tbl}\";")
        cursor.execute("PRAGMA foreign_keys = ON;")
        existing_tables = set()

    needs_schema = force_reseed or not db_exists or not required_tables.issubset(existing_tables)

    if needs_schema:
        if SCHEMA_FILE.exists():
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            cursor.executescript(schema_sql)

        if not db_exists or force_reseed:
            if SEED_FILE.exists():
                with open(SEED_FILE, "r", encoding="utf-8") as f:
                    seed_sql = f.read()
                cursor.executescript(seed_sql)

        conn.commit()
        conn.close()
        print(f"[UMS Database] Successfully initialized and seeded at: {DB_FILE}")
    else:
        conn.close()


def query_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a query and return all matching records as dictionaries."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def query_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """Execute a query and return a single record as a dictionary or None."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def execute_commit(query: str, params: tuple = ()) -> int:
    """Execute an INSERT, UPDATE, or DELETE query and return the lastrowid or affected rows."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
    finally:
        conn.close()


if __name__ == "__main__":
    init_database(force_reseed=True)
    stats = query_all("SELECT name FROM sqlite_master WHERE type='table';")
    print(f"Tables created: {[s['name'] for s in stats]}")
