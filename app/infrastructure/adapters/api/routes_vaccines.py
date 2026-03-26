from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel
from app.infrastructure.adapters.db.models import PetModel
from app.infrastructure.adapters.api.schemas_vaccines import VaccineReminder
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/vaccines", tags=["vaccines"], dependencies=[Depends(get_current_user)])

@router.get("/upcoming", response_model=List[VaccineReminder])
def get_upcoming_vaccines(days: int = 30, db: Session = Depends(get_db)):
    today = datetime.utcnow()
    limit_date = today + timedelta(days=days)
    
    records = db.query(MedicalRecordModel, PetModel)\
        .join(PetModel, MedicalRecordModel.pet_id == PetModel.id)\
        .filter(MedicalRecordModel.next_date >= today)\
        .filter(MedicalRecordModel.next_date <= limit_date)\
        .all()
    
    reminders = []
    for record, pet in records:
        reminders.append(VaccineReminder(
            pet_id=pet.id,
            pet_name=pet.name,
            owner_name="Owner", # We could join with OwnerModel if needed
            record_type=record.record_type,
            next_date=record.next_date
        ))
    
    return reminders
