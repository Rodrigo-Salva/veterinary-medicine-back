from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Appointment:
    id: uuid.UUID
    pet_id: uuid.UUID
    owner_id: uuid.UUID
    date: datetime
    reason: str
    status: str # e.g., "Pending", "Success", "Failed" - matching the reference UI
    cost: float
