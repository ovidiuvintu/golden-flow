import logging
import sys
from fastapi import FastAPI
from controllers.treatments import router as treatments_router
from db import init_db
from services.treatment_service import TreatmentService
import os

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
    init_db(db_path)

    # Initialize services
    app.state.treatment_service = TreatmentService()

    # Include routers under /api so endpoints become /api/treatments
    app.include_router(treatments_router, prefix="/api")

    # Lightweight health endpoint for container healthchecks
    @app.get("/health")
    def _health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "4000")), log_level="info")

