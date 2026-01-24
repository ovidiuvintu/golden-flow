import sqlite3
import os
from typing import Optional, Dict, Any

"""
Module for managing the SQLite database connection and schema initialization.
"""


class Database:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("TREATMENTS_DB_PATH", "treatments.db")

    def get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        conn = self.get_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS treatments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                state TEXT NOT NULL,
                start_time TEXT,
                stop_time TEXT,
                data_file_path TEXT NOT NULL,
                created_at TEXT
            )
            """)
        conn.commit()
        conn.close()

    # Maps a sqlite3.Row to a dictionary using dictionary comprehension
    @staticmethod
    def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        return {k: row[k] for k in row.keys()}
