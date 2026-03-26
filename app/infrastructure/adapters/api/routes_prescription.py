from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.prescription_repository_impl import SqlAlchemyPrescriptionRepository
from app.application.services.prescription_service import PrescriptionUseCase
from app.infrastructure.adapters.api.schemas_prescription import PrescriptionCreate, PrescriptionResponse
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"], dependencies=[Depends(get_current_user)])

def get_prescription_service(db: Session = Depends(get_db)):
    repository = SqlAlchemyPrescriptionRepository(db)
    return PrescriptionUseCase(repository)

@router.post("/", response_model=PrescriptionResponse)
def create_prescription(prescription: PrescriptionCreate, service: PrescriptionUseCase = Depends(get_prescription_service)):
    return service.create_prescription(
        pet_id=prescription.pet_id,
        medications=prescription.medications,
        instructions=prescription.instructions,
        medical_record_id=prescription.medical_record_id
    )

@router.get("/pet/{pet_id}", response_model=List[PrescriptionResponse])
def get_pet_prescriptions(pet_id: UUID, service: PrescriptionUseCase = Depends(get_prescription_service)):
    return service.get_pet_prescriptions(pet_id)

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(prescription_id: UUID, service: PrescriptionUseCase = Depends(get_prescription_service)):
    prescription = service.get_prescription(prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: UUID, service: PrescriptionUseCase = Depends(get_prescription_service)):
    if not service.delete_prescription(prescription_id):
        raise HTTPException(status_code=404, detail="Prescription not found")
    return {"message": "Prescription deleted successfully"}
