from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class PetBase(BaseModel):
    name: str
    species: str
    breed: str
    age: int
    owner_id: uuid.UUID

class PetCreate(PetBase):
    sex: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[float] = None
    allergies: Optional[str] = None
    is_neutered: bool = False
    microchip: Optional[str] = None
    birth_date: Optional[datetime] = None
    notes: Optional[str] = None

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[float] = None
    allergies: Optional[str] = None
    is_neutered: Optional[bool] = None
    microchip: Optional[str] = None
    birth_date: Optional[datetime] = None
    notes: Optional[str] = None

class WeightRecordCreate(BaseModel):
    weight: float
    recorded_date: datetime
    notes: Optional[str] = None

class WeightRecordResponse(BaseModel):
    id: uuid.UUID
    pet_id: uuid.UUID
    weight: float
    recorded_date: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None

class PetResponse(PetBase):
    id: uuid.UUID
    medical_history: Optional[str] = None
    is_active: bool = True
<<<<<<< HEAD
=======
    photo_url: Optional[str] = None
    sex: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[float] = None
    allergies: Optional[str] = None
    is_neutered: bool = False
    microchip: Optional[str] = None
    birth_date: Optional[datetime] = None
    notes: Optional[str] = None
    weight_history: List[WeightRecordResponse] = []
>>>>>>> b509e06 (refactor: enhance user and pet models with extended attributes)

    class Config:
        from_attributes = True

class OwnerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str

class OwnerCreate(OwnerBase):
    pass

class OwnerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class OwnerResponse(OwnerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
    pet_id: uuid.UUID
    owner_id: uuid.UUID
    date: datetime
    reason: str
    cost: float

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: uuid.UUID
    status: str

    class Config:
        from_attributes = True

class MedicalRecordBase(BaseModel):
    description: str
    diagnosis: str
    treatment: str

class MedicalRecordCreate(MedicalRecordBase):
    pet_id: uuid.UUID
    record_type: Optional[str] = "Consultation"
    next_date: Optional[datetime] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: uuid.UUID
    pet_id: uuid.UUID
    recording_date: datetime
    record_type: str
    next_date: Optional[datetime] = None
    vet_id: Optional[uuid.UUID]

    class Config:
        from_attributes = True
