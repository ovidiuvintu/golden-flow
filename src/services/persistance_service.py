import logging
from typing import Optional, Dict, Any, List
from db import get_conn, row_to_dict

# No state therefore no need for a class

logger = logging.getLogger(__name__)

# Inserts treatment info into the database
def insert_treatment(db_path: str, name: str, data_file_path: str) -> Dict[str, Any]:
    conn = get_conn(db_path)
    c = conn.cursor()
    now = __import__('datetime').datetime.utcnow().isoformat()
    c.execute(
        "INSERT INTO treatments (name, description, state, start_time, data_file_path, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (name, None, 'running', now, data_file_path, now),
    )
    conn.commit()
    tid = c.lastrowid
    row = c.execute("SELECT * FROM treatments WHERE id=?", (tid,)).fetchone()
    conn.close()
    return row_to_dict(row)

def update_treatment_state() -> None:
    pass


def get_treatment(db_path: str, treatment_id: int):
    """Return a treatment row dict for the given id, or None if not found."""
    conn = get_conn(db_path)
    row = conn.execute("SELECT * FROM treatments WHERE id=?", (treatment_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return row_to_dict(row)

def list_treatments(db_path: str) -> List[Dict[str, Any]]:
    conn = get_conn(db_path)
    rows = conn.execute("SELECT * FROM treatments ORDER BY id DESC").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

