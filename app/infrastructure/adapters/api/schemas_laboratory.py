from pydantic import BaseModel
from typing import Optional, List, Dict
import uuid
from datetime import datetime

class LaboratoryResultCreate(BaseModel):
    pet_id: uuid.UUID
    test_name: str
    category: str
    notes: Optional[str] = None
    parameters: Optional[str] = None # JSON string

class LaboratoryResultResponse(BaseModel):
    id: uuid.UUID
    pet_id: uuid.UUID
    test_name: str
    category: str
    result_date: datetime
    notes: Optional[str] = None
    parameters: Optional[str] = None

    class Config:
        from_attributes = True
