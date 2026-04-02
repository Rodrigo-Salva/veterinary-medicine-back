from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class LaboratoryResult:
    id: uuid.UUID
    pet_id: uuid.UUID
    test_name: str
    category: str
    result_date: datetime
    notes: Optional[str] = None
    parameters: Optional[str] = None # JSON string
