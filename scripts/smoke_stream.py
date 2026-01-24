import sys
import asyncio
import time

# Ensure src is on path
sys.path.insert(0, "src")

from services.persistence_service import PersistenceService
from services.simulation_service import SimulationService
from services.mqtt_service import MqttService
from db import Database


async def run_and_cancel():
    # Ensure DB schema exists
    Database().init_db()
    p = PersistenceService()
    # Insert a transient treatment record pointing to the high-fidelity CSV
    rec = p.insert_treatment(
        "smoke-test", "src/high_fidelity_fracturing_sample_12000_rows.csv"
    )
    tid = rec["id"]
    sim = SimulationService(persistence=p, publisher=MqttService())
    task = asyncio.create_task(sim.start_streaming(tid))
    # Let it stream for a few seconds then cancel
    await asyncio.sleep(3)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Smoke stream cancelled after 3 seconds")


if __name__ == "__main__":
    asyncio.run(run_and_cancel())
