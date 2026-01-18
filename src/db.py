
import sqlite3
import os
from typing import Optional, Dict, Any

def get_conn(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or os.getenv("TREATMENTS_DB_PATH", "treatments.db")
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Optional[str] = None) -> None:
    conn = get_conn(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            state TEXT NOT NULL,
            start_time TEXT,
            stop_time TEXT,
            data_file_path TEXT NOT NULL,
            created_at TEXT,
            last_processed_row INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}
