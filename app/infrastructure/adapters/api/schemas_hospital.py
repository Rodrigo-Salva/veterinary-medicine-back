from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
import uuid

class CageBase(BaseModel):
    name: str

class CageCreate(CageBase):
    pass

class CageUpdate(CageBase):
    pass

class CageResponse(CageBase):
    id: uuid.UUID
    is_occupied: bool
    current_pet_id: Optional[uuid.UUID]
    current_hospitalization_id: Optional[uuid.UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

class VitalSignBase(BaseModel):
    temperature: float
    heart_rate: int
    respiratory_rate: int
    notes: str

class VitalSignCreate(VitalSignBase):
    hospitalization_id: uuid.UUID

class VitalSignResponse(VitalSignBase):
    id: uuid.UUID
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class HospitalizationBase(BaseModel):
    pet_id: uuid.UUID
    cage_id: uuid.UUID
    reason: str

class HospitalizationCreate(HospitalizationBase):
    pass

class HospitalizationResponse(HospitalizationBase):
    id: uuid.UUID
    check_in_date: datetime
    check_out_date: Optional[datetime]
    status: str
    vital_signs: List[VitalSignResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
