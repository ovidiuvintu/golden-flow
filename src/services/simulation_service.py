import csv
import asyncio
import logging
from typing import Optional
from db import Database
from services.persistence_service import PersistenceService
from services.mqtt_service import MqttService

logger = logging.getLogger(__name__)

'''
Module for reading data file (csv) from docker storage one row at the time
at 1 second intervals and publishing each row as a json message to MQTT broker.
'''

'''
TODO: Depends on PersistenceService and MqttService concrete implementations
      Should depend on abstractions instead (SOLID principle)
'''

class SimulationService:
    
    def __init__(self, persistence: Optional[PersistenceService] = None, publisher: Optional[MqttService] = None):
        self.persistence = persistence or PersistenceService()
        self.publisher = publisher or MqttService()

    async def start_streaming(self, treatment_id: int):
        logger.info("Initiating streaming for treatment ID: %s", treatment_id)
        # fetch treatment info from the database
        treatment = self.persistence.get_treatment(treatment_id)
        if not treatment:
            logger.error("Treatment not found for streaming: %s", treatment_id)
            return
        # get the path to the simulation data file
        path = treatment["data_file_path"]

        logger.info("Starting streaming for treatment %s from file %s", treatment_id, path)
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_index, row in enumerate(reader, start=1):
                await asyncio.sleep(1)  # Simulate 1 second delay between messages

                try:
                    # Use column names provided by the CSV header
                    timestamp = int(row["timestamp_unix"])
                    volume = float(row["volume_gallons"])
                    pressure = float(row["pressure_psi"])

                    # convert to json format
                    payload = {"treatment_id": treatment_id, "timestamp": timestamp, "volume": volume, "pressure": pressure}
                    # Publish to MQTT
                    self.publisher.publish(f"treatments/{treatment_id}", payload)
                except Exception:
                    logger.exception("Malformed CSV row at idx %s: %s", row_index, row)
                    continue


