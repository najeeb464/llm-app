

import sqlite3
import os
from datetime import datetime
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traces.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            category TEXT NOT NULL,
            response_time REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_trace(
    user_message: str,
    bot_response: str,
    category: str,
    response_time: float,
) -> dict:
    """Insert a new trace and return it as a dictionary."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute(
        """
        INSERT INTO traces (user_message, bot_response, category, response_time, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_message, bot_response, category, response_time, timestamp),
    )
    conn.commit()
    trace_id = cursor.lastrowid
    conn.close()
    return {
        "id": trace_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "category": category,
        "response_time": response_time,
        "timestamp": timestamp,
    }


def get_traces(category: Optional[str] = None) -> list[dict]:
    """Return all traces"""
    conn = get_connection()
    cursor = conn.cursor()
    if category:
        cursor.execute(
            "SELECT * FROM traces WHERE category = ? ORDER BY id DESC",
            (category,),
        )
    else:
        cursor.execute("SELECT * FROM traces ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_analytics() -> dict:
    """Return aggregate stats."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total count
    cursor.execute("SELECT COUNT(*) as total FROM traces")
    total = cursor.fetchone()["total"]

    # Category breakdown
    cursor.execute(
        """
        SELECT category, COUNT(*) as count
        FROM traces
        GROUP BY category
        ORDER BY count DESC
        """
    )
    categories = []
    for row in cursor.fetchall():
        categories.append(
            {
                "name": row["category"],
                "count": row["count"],
                "percentage": round((row["count"] / total) * 100, 1) if total > 0 else 0,
            }
        )

    # Average response time
    cursor.execute("SELECT AVG(response_time) as avg_rt FROM traces")
    avg_rt_row = cursor.fetchone()
    avg_response_time = round(avg_rt_row["avg_rt"], 3) if avg_rt_row["avg_rt"] else 0

    conn.close()
    return {
        "total": total,
        "categories": categories,
        "avg_response_time": avg_response_time,
    }
