from pathlib import Path
import os
import logging
import asyncio
from typing import Dict, Optional, Any
import uuid
from fastapi import UploadFile

from db import Database
from services.persistence_service import PersistenceService
from services.simulation_service import SimulationService
from services.storage_service import StorageService
from services.mqtt_service import MqttService

logger = logging.getLogger(__name__)

"""
Module for managing all treatment operations
"""


class TreatmentService:
    def __init__(
        self,
        db_path: Optional[str] = None,
        storage: Optional[StorageService] = None,
        persistence: Optional[PersistenceService] = None,
        simulation: Optional[SimulationService] = None,
        publisher: Optional[MqttService] = None,
    ):
        self.db_path = db_path or os.getenv("TREATMENTS_DB_PATH", "treatments.db")
        Database(self.db_path).init_db()
        self.tasks: Dict[int, asyncio.Task] = {}
        self.storage = storage or StorageService()
        self.persistence = persistence or PersistenceService(Database(self.db_path))
        self.publisher = publisher or MqttService()
        self.simulation = simulation or SimulationService(
            self.persistence, self.publisher
        )

    # Public interface methods
    def list_treatments(self):
        return self.persistence.list_treatments()

    async def start_treatment(
        self, name: str, upload_file: UploadFile
    ) -> Dict[str, Any]:
        # Delegate file saving to StorageService
        target_path = await self.storage.save_upload(upload_file)

        # save treatment info to the database and get the treatment record
        treatment = self._insert_treatment(name, target_path)
        # get the treatment ID which will be used as an identifer for this treatment streaming
        treatmentId = int(treatment["id"])

        # Start background streaming task.
        loop = asyncio.get_running_loop()
        logger.info(f"Starting streaming task for treatment {treatmentId}")

        # run concurrently on the event loop. gives you a false sense
        # of parallelism. No parrallelism here since Python has GIL.
        task = loop.create_task(self._stream_worker(treatmentId))
        self.tasks[treatmentId] = task

        return treatment

    # TODO: Implement these methods
    def stop_treatment(self) -> None:
        pass

    def change_state(self) -> None:
        pass

    # Private helper methods

    def _insert_treatment(self, name: str, data_file_path: str) -> Dict[str, Any]:
        return self.persistence.insert_treatment(name, data_file_path)

    def _update_treatment_state(self) -> None:
        pass

    def _get_treatment(self) -> None:
        pass

    async def _stream_worker(self, treatment_id: int):
        # Delegate streaming to the injected SimulationService
        await self.simulation.start_streaming(treatment_id)
