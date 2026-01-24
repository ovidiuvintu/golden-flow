import logging
import sys
from fastapi import FastAPI
from controllers.treatments import router as treatments_router
from db import Database
from services.treatment_service import TreatmentService
from services.storage_service import StorageService
from services.persistence_service import PersistenceService
from services.simulation_service import SimulationService
from services.mqtt_service import MqttService
import os

"""
   Application entry point setting up FastAPI app, 
   initializing services, and wiring dependencies.
"""
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    logger.info("Application started")

    app = FastAPI(title="Treatment Simulation")

    # Initialize DB
    db_path = os.getenv("TREATMENTS_DB_PATH", "treatments.db")
    Database(db_path).init_db()

    # Initialize services and inject dependencies
    storage = StorageService()
    db = Database(db_path)
    persistence = PersistenceService(db)
    mqtt = MqttService()
    simulation = SimulationService(persistence=persistence, publisher=mqtt)
    app.state.treatment_service = TreatmentService(
        db_path=db_path,
        storage=storage,
        persistence=persistence,
        simulation=simulation,
        publisher=mqtt,
    )

    # Include routers under /api by convention
    # TODO: Add versioning later
    app.include_router(treatments_router, prefix="/api")

    # health endpoint for container healthchecks
    @app.get("/health")
    def _health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=int(os.getenv("PORT", "4000")), log_level="info"
    )
