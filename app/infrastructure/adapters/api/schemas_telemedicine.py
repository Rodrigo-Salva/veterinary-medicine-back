from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class TelemedicineSessionBase(BaseModel):
    appointment_id: uuid.UUID
    pet_id: uuid.UUID
    doctor_name: str
    pet_name: str
    room_url: str

class TelemedicineSessionCreate(BaseModel):
    appointment_id: uuid.UUID
    pet_id: uuid.UUID

class TelemedicineSessionResponse(TelemedicineSessionBase):
    id: uuid.UUID
    status: str # 'scheduled', 'active', 'completed'
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    sender: str
    content: str
    timestamp: datetime
