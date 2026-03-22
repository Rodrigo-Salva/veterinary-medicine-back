from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.adapters.db.database import Base
import uuid
from datetime import datetime

class MedicalRecordModel(Base):
    __tablename__ = "medical_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    recording_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=False)
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    record_type = Column(String, default="Consultation") # "Consultation", "Vaccine", "Check-up"
    next_date = Column(DateTime, nullable=True) # For vaccine/next visit reminders
    vet_id = Column(UUID(as_uuid=True), nullable=True)

class PrescriptionModel(Base):
    __tablename__ = "prescriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    medical_record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.id"), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    medications = Column(Text, nullable=False) # Simple text for now, or JSON string
    instructions = Column(Text, nullable=False)
