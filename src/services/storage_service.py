from pathlib import Path
import os
import uuid
import logging
from typing import Optional
from fastapi import UploadFile

logger = logging.getLogger(__name__)

'''
Module for copying the local data file (csv) to docker internal
storage. 
TODO: Need to use docker volumes.
SOLID principle implemented: Single Responsibility Principle
'''
class StorageService:
    def __init__(self, uploads_dir: Optional[str] = None):
        self.uploads_dir = uploads_dir or os.path.join(os.getcwd(), "data")
        os.makedirs(self.uploads_dir, exist_ok=True)

    async def save_upload(self, upload_file: UploadFile) -> str:
        # Save an UploadFile to the uploads directory and return the file path.
        filename = f"{uuid.uuid4().hex}-{upload_file.filename}"
        target_path = os.path.join(self.uploads_dir, filename)
        logger.info("Saving upload to %s", target_path)
        content = await upload_file.read()
        with open(target_path, "wb") as out_f:
            out_f.write(content)
        return target_path
