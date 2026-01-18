from fastapi import FastAPI
from src.controllers.treatments import router as treatments_router
from src.db import init_db
from src.services.treatment_service import TreatmentService
import os

def create_app() -> FastAPI:
    app = FastAPI(title="Treatment Simulation")

    # Initialize DB
    db_path = os.getenv("TREATMENTS_DB_PATH", "treatments.db")
    init_db(db_path)

    # Initialize services
    app.state.treatment_service = TreatmentService()

    # Include routers
    app.include_router(treatments_router, prefix="/api/treatments")

    app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=4002, reload=True)
