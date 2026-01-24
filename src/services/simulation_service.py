import csv
import asyncio
import logging
from datetime import datetime
from typing import Optional
from db import Database
from services.persistence_service import PersistenceService
from services.mqtt_service import MqttService

logger = logging.getLogger(__name__)

"""
Module for reading data file (csv) from docker storage one row at the time
at 1 second intervals and publishing each row as a json message to MQTT broker.
"""

"""
TODO: Depends on PersistenceService and MqttService concrete implementations
      Should depend on abstractions instead (SOLID principle)
"""


class SimulationService:

    def __init__(
        self,
        persistence: Optional[PersistenceService] = None,
        publisher: Optional[MqttService] = None,
    ):
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
        # Disallow the old sample file - require high-fidelity sample
        if path.endswith("simulation_data.csv"):
            logger.error(
                "Legacy sample file 'simulation_data.csv' is no longer supported. Use high_fidelity_fracturing_sample_12000_rows.csv instead."
            )
            return

        logger.info(
            "Starting streaming for treatment %s from file %s", treatment_id, path
        )
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Validate schema: expect at minimum a 'timestamp' column
            headers = reader.fieldnames or []
            if "timestamp" not in headers:
                logger.error(
                    "Unsupported CSV schema: missing 'timestamp' header in %s", path
                )
                return

            for row_index, row in enumerate(reader, start=1):
                await asyncio.sleep(1)  # Simulate 1 second delay between messages

                try:
                    # Parse timestamp (example format: '1/1/2026 6:00')
                    raw_ts = row.get("timestamp", "")
                    try:
                        dt = datetime.strptime(raw_ts, "%m/%d/%Y %H:%M")
                    except ValueError:
                        # Try ISO fallback
                        dt = datetime.fromisoformat(raw_ts)
                    timestamp = int(dt.timestamp())

                    # Build payload from available high-fidelity columns (pick a sensible subset)
                    payload = {"treatment_id": treatment_id, "timestamp": timestamp}

                    # Common numeric fields if present
                    numeric_fields = [
                        "treating_pressure_psi",
                        "casing_pressure_psi",
                        "hydrostatic_pressure_psi",
                        "pump_rate_bpm",
                        "slurry_rate_bpm",
                        "sand_concentration_ppg",
                        "temperature_f",
                    ]
                    for field in numeric_fields:
                        if field in row and row[field] not in (None, ""):
                            try:
                                payload[field] = float(row[field])
                            except ValueError:
                                # keep original string if conversion fails
                                payload[field] = row[field]

                    # include any event flag or stage if present
                    if "event_flag" in row:
                        payload["event_flag"] = row["event_flag"]
                    if "stage" in row:
                        try:
                            payload["stage"] = int(row["stage"])
                        except ValueError:
                            payload["stage"] = row["stage"]

                    # Publish to MQTT
                    self.publisher.publish(f"treatments/{treatment_id}", payload)
                except Exception:
                    logger.exception("Malformed CSV row at idx %s: %s", row_index, row)
                    continue
