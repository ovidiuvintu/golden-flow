
from pathlib import Path
import os
import logging
from typing import Dict, Optional, Any
import uuid
from fastapi import UploadFile

from db import init_db
from services import persistance_service as persistence

logger = logging.getLogger(__name__)

class TreatmentService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.getenv("TREATMENTS_DB_PATH", "treatments.db")
        init_db(self.db_path)

    # Public interface methods
    def list_treatments(self):
        return persistence.list_treatments(self.db_path)
    
    async def start_treatment(self, name: str, upload_file: UploadFile) -> Dict[str, Any]:
        # copy the local file to docker data directory
        uploads_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(uploads_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}-{upload_file.filename}"
        target_path = os.path.join(uploads_dir, filename)

        # Save upload to docker data directory
        with open(target_path, "wb") as out_f:
            content = await upload_file.read()
            out_f.write(content)

        logger.info(f"Saved uploaded file to {target_path}")
        
        # save treatment info to the database
        treatment = self._insert_treatment(name, target_path)
        return treatment

    def stop_treatment(self) -> None:
        pass 

    def change_state(self) -> None:
        pass      
    
    # Private helper methods
    def _insert_treatment(self, name: str, data_file_path: str) -> Dict[str, Any]:
        return persistence.insert_treatment(self.db_path, name, data_file_path)

    def _update_treatment_state(self) -> None:
       pass

    def _get_treatment(self) -> None:
        pass

    def _stream_worker(self) -> None:
        pass
