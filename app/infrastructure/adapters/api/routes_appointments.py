from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.appointment_repository_impl import SqlAlchemyAppointmentRepository
from app.application.services.schedule_appointment import ScheduleAppointmentUseCase
from app.infrastructure.adapters.api.schemas import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    repository = SqlAlchemyAppointmentRepository(db)
    use_case = ScheduleAppointmentUseCase(repository)
    return use_case.execute(
        pet_id=appointment.pet_id,
        owner_id=appointment.owner_id,
        date=appointment.date,
        reason=appointment.reason,
        cost=appointment.cost
    )

@router.get("/", response_model=List[AppointmentResponse])
def list_appointments(db: Session = Depends(get_db)):
    repository = SqlAlchemyAppointmentRepository(db)
    return repository.find_all()

@router.get("/pet/{pet_id}", response_model=List[AppointmentResponse])
def get_appointments_by_pet(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyAppointmentRepository(db)
    return repository.find_by_pet(pet_id)
