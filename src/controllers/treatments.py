
# Controller for managing treatments
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from models.schemas import TreatmentOut
from typing import List
import logging

# Configure the logger at the module level
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency to get the treatment service
# FastApi's dependency injection system can be used to manage service instances.
def get_service(request: Request):
    return request.app.state.treatment_service

# Endpoint to start a new treatment
# Form() used for automatic data validation and comprehensive error handling. 
# If the data doesn't match the defined schema, FastAPI returns a 422 Unprocessable Entity error
@router.post("/treatments", status_code=201)
async def start_treatment_async(name: str = Form(...), file: UploadFile = File(...), request: Request = None):
    svc = get_service(request)
    if not name:
        raise HTTPException(status_code=400, detail="Treatment name is required")
    treatment = await svc.start_treatment(name, file)
    return JSONResponse(status_code=201, content=treatment)

# Endpoint to list all treatments
@router.get("/treatments", response_model=List[TreatmentOut])
async def list_treatments(request: Request):
    svc = get_service(request)
    return svc.list_treatments()

# Endpoint to get a specific treatment by ID
@router.get("/treatments/{id}")
def get_treatment(id: int, request: Request):
    svc = get_service(request)
    treatment = svc.persistence.get_treatment(id)
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment