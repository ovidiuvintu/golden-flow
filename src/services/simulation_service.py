import csv
import asyncio
import logging
from typing import Optional
from services import persistance_service as persistence
# No state therefore no need for a class

logger = logging.getLogger(__name__)

async def start_streaming(db_path: str, treatment_id: int):
    treatment = persistence.get_treatment(db_path, treatment_id)
    if not treatment:
        logger.error("Treatment not found for streaming: %s", treatment_id)
        return
    # get the path to the simulation data file
    path = treatment["data_file_path"]

    logger.info("Starting streaming for treatment %s from file %s", treatment_id, path)
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row_index, row in enumerate(reader, start=1):
            # Read each row and log it. In real implementation, publish to MQTT
            logger.info("Streaming data for treatment %s: %s", treatment_id, row)
            await asyncio.sleep(1)  # Simulate 1 second delay between messages

            try:
                timestamp = int(row[0])
                volume = float(row[1])
                pressure = float(row[2])
                # Here you would publish to MQTT instead of logging
                logger.info("Published to MQTT - Treatment %s: timestamp=%s, volume=%s, pressure=%s",
                             treatment_id, timestamp, volume, pressure)
            except Exception:
                logger.exception("Malformed CSV row at idx %s: %s", row_index, row)
                continue
