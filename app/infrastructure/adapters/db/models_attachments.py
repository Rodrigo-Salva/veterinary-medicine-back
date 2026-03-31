from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.adapters.db.database import Base
import uuid
from datetime import datetime

class AttachmentModel(Base):
    __tablename__ = "medical_attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    medical_record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.id"), nullable=True)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False) # "Image", "PDF", "Other"
    description = Column(String, nullable=True)
    category = Column(String, nullable=False, default="General") # "Laboratory", "X-Ray", "Ultrasound", "General"
    upload_date = Column(DateTime, default=datetime.utcnow)
