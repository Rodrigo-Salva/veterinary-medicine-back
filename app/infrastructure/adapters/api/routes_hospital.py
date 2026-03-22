from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.hospital_repository_impl import SqlAlchemyHospitalizationRepository
from app.application.services.hospitalization_service import HospitalizationUseCase
from app.infrastructure.adapters.api.schemas_hospital import (
    CageResponse, HospitalizationCreate, HospitalizationResponse, VitalSignCreate, VitalSignResponse
)

router = APIRouter(prefix="/hospital", tags=["hospital"])

@router.get("/cages", response_model=List[CageResponse])
def list_cages(db: Session = Depends(get_db)):
    repo = SqlAlchemyHospitalizationRepository(db)
    return repo.get_cages()

@router.post("/check-in", response_model=HospitalizationResponse)
def check_in(data: HospitalizationCreate, db: Session = Depends(get_db)):
    repo = SqlAlchemyHospitalizationRepository(db)
    use_case = HospitalizationUseCase(repo)
    try:
        return use_case.check_in(data.pet_id, data.cage_id, data.reason)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/vitals", response_model=VitalSignResponse)
def record_vitals(data: VitalSignCreate, db: Session = Depends(get_db)):
    repo = SqlAlchemyHospitalizationRepository(db)
    use_case = HospitalizationUseCase(repo)
    return use_case.record_vitals(
        data.hospitalization_id, data.temperature, 
        data.heart_rate, data.respiratory_rate, data.notes
    )

@router.post("/discharge/{hosp_id}", response_model=HospitalizationResponse)
def discharge(hosp_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = SqlAlchemyHospitalizationRepository(db)
    use_case = HospitalizationUseCase(repo)
    try:
        return use_case.discharge(hosp_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{hosp_id}", response_model=HospitalizationResponse)
def get_hospitalization(hosp_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = SqlAlchemyHospitalizationRepository(db)
    h = repo.get_hospitalization_by_id(hosp_id)
    if not h:
        raise HTTPException(status_code=404, detail="Hospitalization not found")
    return h
