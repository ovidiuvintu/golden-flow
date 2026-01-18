
import sys
from pathlib import Path
import asyncio
import csv
import sqlite3
import os
import logging
from typing import Optional

from db import init_db
from services import persistance_service as persistence

logger = logging.getLogger(__name__)

class TreatmentService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("TREATMENTS_DB_PATH", "treatments.db")
        init_db(self.db_path)

    # Public interface methods
    def list_treatments(self):
        return persistence.list_treatments()
    
    async def start_treatment(self) -> None:
        pass

    def stop_treatment(self) -> None:
        pass 

    def change_state(self) -> None:
        pass      
    
    # Private helper methods
    def _insert_treatment(self) -> None:
        pass

    def _update_treatment_state(self) -> None:
       pass

    def _get_treatment(self) -> None:
        pass

    def _stream_worker(self) -> None:
        pass
