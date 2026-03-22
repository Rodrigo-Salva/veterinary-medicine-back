from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import List, Optional

@dataclass
class Cage:
    id: uuid.UUID
    name: str  # e.g., "Cage A1", "Large Dog B"
    is_occupied: bool = False
    current_pet_id: Optional[uuid.UUID] = None

@dataclass
class VitalSignRecord:
    id: uuid.UUID
    hospitalization_id: uuid.UUID
    timestamp: datetime
    temperature: float
    heart_rate: int
    respiratory_rate: int
    notes: str

@dataclass
class Hospitalization:
    id: uuid.UUID
    pet_id: uuid.UUID
    cage_id: uuid.UUID
    check_in_date: datetime
    reason: str
    check_out_date: Optional[datetime] = None
    status: str = "Active" # Active, Discharged
    vital_signs: List[VitalSignRecord] = field(default_factory=list)
