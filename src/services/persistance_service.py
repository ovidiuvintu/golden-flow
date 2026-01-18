import logging
from typing import Optional, Dict, Any, List
from src.db import get_conn, row_to_dict

# No state therefore no need for a class

logger = logging.getLogger(__name__)

def insert_treatment() -> None:
    pass

def update_treatment_state() -> None:
    pass

def get_treatment() -> None:
    pass

def list_treatments(db_path: str) -> List[Dict[str, Any]]:
    conn = get_conn(db_path)
    rows = conn.execute("SELECT * FROM treatments ORDER BY id DESC").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

