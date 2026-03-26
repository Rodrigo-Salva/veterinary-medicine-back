from pydantic import BaseModel
from datetime import datetime
import uuid


class VaccineReminder(BaseModel):
    pet_id: uuid.UUID
    pet_name: str
    owner_name: str
    record_type: str
    next_date: datetime
