from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel
from app.infrastructure.adapters.db.models_hospital import CageModel, HospitalizationModel, VitalSignModel
from app.infrastructure.adapters.db.models_inventory import ProductModel
from app.infrastructure.adapters.db.models_user import UserModel
from sqlalchemy.dialects.postgresql import UUID
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

class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, nullable=False) # "Pending", "Success", "Failed"
    cost = Column(Float, nullable=False)
