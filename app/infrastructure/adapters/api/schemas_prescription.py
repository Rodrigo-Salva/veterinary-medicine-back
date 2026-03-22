from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class PrescriptionBase(BaseModel):
    pet_id: uuid.UUID
    medications: str
    instructions: str
    medical_record_id: Optional[uuid.UUID] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionResponse(PrescriptionBase):
    id: uuid.UUID
    date: datetime

    class Config:
        from_attributes = True
