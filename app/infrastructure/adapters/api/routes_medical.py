from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.medical_record_repository_impl import SqlAlchemyMedicalRecordRepository
from app.application.services.add_medical_record import AddMedicalRecordUseCase
from app.infrastructure.adapters.api.schemas import MedicalRecordCreate, MedicalRecordResponse

router = APIRouter(prefix="/medical-records", tags=["medical-records"])

@router.post("/", response_model=MedicalRecordResponse)
def create_medical_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    repository = SqlAlchemyMedicalRecordRepository(db)
    use_case = AddMedicalRecordUseCase(repository)
    return use_case.execute(
        pet_id=record.pet_id,
        description=record.description,
        diagnosis=record.diagnosis,
        treatment=record.treatment
    )

@router.get("/pet/{pet_id}", response_model=List[MedicalRecordResponse])
def get_medical_history(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyMedicalRecordRepository(db)
    return repository.find_by_pet_id(pet_id)
