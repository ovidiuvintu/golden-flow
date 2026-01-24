import logging
from typing import Optional, Dict, Any, List
from db import Database

logger = logging.getLogger(__name__)


"""
Module for persistence service for treatments DB operations.
"""


class PersistenceService:

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()

    def _conn(self):
        return self.db.get_conn()

    def insert_treatment(self, name: str, data_file_path: str) -> Dict[str, Any]:
        conn = self._conn()
        c = conn.cursor()
        now = __import__("datetime").datetime.utcnow().isoformat()
        c.execute(
            "INSERT INTO treatments (name, description, state, start_time, data_file_path, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name, None, "running", now, data_file_path, now),
        )
        conn.commit()
        tid = c.lastrowid
        row = c.execute("SELECT * FROM treatments WHERE id=?", (tid,)).fetchone()
        conn.close()
        return Database.row_to_dict(row)

    def update_treatment_state(self) -> None:
        pass

    def get_treatment(self, treatment_id: int):
        """
        Return a treatment row dict for the given id, or
        None if not found.
        """
        conn = self._conn()
        row = conn.execute(
            "SELECT * FROM treatments WHERE id=?", (treatment_id,)
        ).fetchone()
        conn.close()
        if not row:
            return None
        return Database.row_to_dict(row)

    def list_treatments(self) -> List[Dict[str, Any]]:
        conn = self._conn()
        rows = conn.execute("SELECT * FROM treatments ORDER BY id DESC").fetchall()
        conn.close()
        return [Database.row_to_dict(r) for r in rows]
