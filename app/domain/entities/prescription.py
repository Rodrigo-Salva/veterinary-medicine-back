from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

@dataclass
class Prescription:
    id: UUID
    pet_id: UUID
    medical_record_id: Optional[UUID]
    date: datetime
    medications: str
    instructions: str

    @classmethod
    def create(cls, pet_id: UUID, medications: str, instructions: str, medical_record_id: Optional[UUID] = None):
        return cls(
            id=uuid4(),
            pet_id=pet_id,
            medical_record_id=medical_record_id,
            date=datetime.utcnow(),
            medications=medications,
            instructions=instructions
        )
