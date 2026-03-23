from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.appointment_repository_impl import SqlAlchemyAppointmentRepository
from app.infrastructure.adapters.db.models import AppointmentModel
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

@router.get("/range", response_model=List[AppointmentResponse])
def list_appointments_by_range(
    start: datetime,
    end: datetime,
    db: Session = Depends(get_db)
):
    appts = db.query(AppointmentModel).filter(
        AppointmentModel.date >= start,
        AppointmentModel.date <= end
    ).order_by(AppointmentModel.date).all()
    return appts

@router.get("/pet/{pet_id}", response_model=List[AppointmentResponse])
def get_appointments_by_pet(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyAppointmentRepository(db)
    return repository.find_by_pet(pet_id)

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: uuid.UUID, data: AppointmentCreate, db: Session = Depends(get_db)):
    appt = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.pet_id = data.pet_id
    appt.owner_id = data.owner_id
    appt.date = data.date
    appt.reason = data.reason
    appt.cost = data.cost
    db.commit()
    db.refresh(appt)
    return appt

@router.patch("/{appointment_id}/status")
def update_appointment_status(appointment_id: uuid.UUID, status: str, db: Session = Depends(get_db)):
    appt = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if status not in ["Pending", "Success", "Failed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    appt.status = status
    db.commit()
    db.refresh(appt)
    return appt

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: uuid.UUID, db: Session = Depends(get_db)):
    appt = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"message": "Appointment deleted"}

