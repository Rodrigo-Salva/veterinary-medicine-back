from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class AttachmentResponse(BaseModel):
    id: uuid.UUID
    pet_id: uuid.UUID
    file_path: str
    file_type: str
    description: Optional[str]
    category: str
    upload_date: datetime

    class Config:
        from_attributes = True
