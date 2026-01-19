import csv
import asyncio
import logging
from typing import Optional
from services import persistance_service as persistence
# No state therefore no need for a class KISS

logger = logging.getLogger(__name__)

async def start_streaming(db_path: str, treatment_id: int):
    logger.info("Initiating streaming for treatment ID: %s", treatment_id)
    # fetch treatment info from the database
    treatment = persistence.get_treatment(db_path, treatment_id)
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
                # Here you would publish to MQTT instead of logging
                logger.info(
                    "Treatment %s: timestamp=%s, volume=%s, pressure=%s",
                    treatment_id,
                    timestamp,
                    volume,
                    pressure,
                )
            except Exception:
                logger.exception("Malformed CSV row at idx %s: %s", row_index, row)
                continue
