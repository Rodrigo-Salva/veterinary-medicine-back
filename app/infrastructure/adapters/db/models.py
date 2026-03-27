<<<<<<< HEAD
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Boolean
=======
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Boolean, Date, Text
>>>>>>> b509e06 (refactor: enhance user and pet models with extended attributes)
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel
from app.infrastructure.adapters.db.models_hospital import CageModel, HospitalizationModel, VitalSignModel
from app.infrastructure.adapters.db.models_inventory import ProductModel
from app.infrastructure.adapters.db.models_user import UserModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.adapters.db.database import Base
import uuid


class OwnerModel(Base):
    __tablename__ = "owners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    medical_history = Column(String, nullable=True)
<<<<<<< HEAD
    is_active = Column(Boolean, nullable=False, default=True, server_default='true')
=======
    is_active = Column(Boolean, default=True)
    photo_url = Column(String, nullable=True)
    sex = Column(String(10), nullable=True)
    color = Column(String(50), nullable=True)
    weight = Column(Float, nullable=True)
    allergies = Column(Text, nullable=True)
    is_neutered = Column(Boolean, default=False)
    microchip = Column(String(50), nullable=True)
    birth_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    weight_records = relationship("WeightRecordModel", back_populates="pet", order_by="WeightRecordModel.recorded_date.desc()")


class WeightRecordModel(Base):
    __tablename__ = "weight_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Float, nullable=False)
    recorded_date = Column(Date, nullable=False)
    notes = Column(String(200), nullable=True)

    pet = relationship("PetModel", back_populates="weight_records")

>>>>>>> b509e06 (refactor: enhance user and pet models with extended attributes)

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, nullable=False)  # "Pending", "Success", "Failed"
    cost = Column(Float, nullable=False)
