from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Optional

@dataclass
class MedicalRecord:
    id: uuid.UUID
    pet_id: uuid.UUID
    recording_date: datetime
    description: str
    diagnosis: str
    treatment: str
    record_type: str = "Consultation"
    next_date: Optional[datetime] = None
    vet_id: Optional[uuid.UUID] = None
