# use the pydatic library define data models (schemas) with type validation

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# Enum for treatment states. Defines possible states for a treatment process.
class TreatmentState(str, Enum):
    running = "running"
    paused = "paused"
    error = "error"
    done = "done"


# Schema for creating a new treatment
class TreatmentCreate(BaseModel):
    # The name of the treatment with a maximum length of 100 characters
    # Required Field with Metadata: Use ... as the first argument in Field() to specify a field
    # is required while still adding extra configuration like descriptions or validation constraints.
    name: str = Field(..., max_length=100)


# Schema for an existing treatment
# Pydantic BaseModel raises a ValidationError exception if the data provided does not conform to the defined types and constraints.
class TreatmentOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    state: TreatmentState
    start_time: Optional[str]
    stop_time: Optional[str]
    data_file_path: str
    created_at: Optional[str]
