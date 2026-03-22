from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class Pet:
    id: uuid.UUID
    name: str
    species: str
    breed: str
    age: int
    owner_id: uuid.UUID
    medical_history: Optional[str] = None
