from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date
import uuid


@dataclass
class WeightRecord:
    id: uuid.UUID
    pet_id: uuid.UUID
    weight: float
    recorded_date: date
    notes: Optional[str] = None


@dataclass
class Pet:
    id: uuid.UUID
    name: str
    species: str
    breed: str
    age: int
    owner_id: uuid.UUID
    medical_history: Optional[str] = None
    is_active: bool = True
    photo_url: Optional[str] = None
    sex: Optional[str] = None  # "Macho", "Hembra"
    color: Optional[str] = None
    weight: Optional[float] = None
    allergies: Optional[str] = None
    is_neutered: bool = False
    microchip: Optional[str] = None
    birth_date: Optional[date] = None
    notes: Optional[str] = None
    weight_history: List[WeightRecord] = field(default_factory=list)
