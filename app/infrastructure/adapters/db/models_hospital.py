from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.adapters.db.database import Base
import uuid
from datetime import datetime

class CageModel(Base):
    __tablename__ = "cages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    is_occupied = Column(Boolean, default=False)
    current_pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=True)

class VitalSignModel(Base):
    __tablename__ = "vital_signs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hospitalization_id = Column(UUID(as_uuid=True), ForeignKey("hospitalizations.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    heart_rate = Column(Integer)
    respiratory_rate = Column(Integer)
    notes = Column(Text)

class HospitalizationModel(Base):
    __tablename__ = "hospitalizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    cage_id = Column(UUID(as_uuid=True), ForeignKey("cages.id"), nullable=False)
    check_in_date = Column(DateTime, default=datetime.utcnow)
    check_out_date = Column(DateTime, nullable=True)
    reason = Column(Text, nullable=False)
    status = Column(String, default="Active")
