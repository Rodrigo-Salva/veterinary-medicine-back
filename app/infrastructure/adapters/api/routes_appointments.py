from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.appointment_repository_impl import SqlAlchemyAppointmentRepository
from app.application.services.schedule_appointment import ScheduleAppointmentUseCase
from app.infrastructure.adapters.api.schemas import AppointmentCreate, AppointmentResponse
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["appointments"], dependencies=[Depends(get_current_user)])

VALID_STATUSES = {"Pending", "Success", "Failed"}


def get_repo(db: Session = Depends(get_db)) -> SqlAlchemyAppointmentRepository:
    return SqlAlchemyAppointmentRepository(db)


@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, repo: SqlAlchemyAppointmentRepository = Depends(get_repo)):
    use_case = ScheduleAppointmentUseCase(repo)
    return use_case.execute(
        pet_id=appointment.pet_id,
        owner_id=appointment.owner_id,
        date=appointment.date,
        reason=appointment.reason,
        cost=appointment.cost,
    )


@router.get("/", response_model=List[AppointmentResponse])
def list_appointments(repo: SqlAlchemyAppointmentRepository = Depends(get_repo)):
    return repo.find_all()


@router.get("/range", response_model=List[AppointmentResponse])
def list_appointments_by_range(
    start: datetime,
    end: datetime,
    repo: SqlAlchemyAppointmentRepository = Depends(get_repo),
):
    return repo.find_by_range(start, end)


@router.get("/pet/{pet_id}", response_model=List[AppointmentResponse])
def get_appointments_by_pet(pet_id: uuid.UUID, repo: SqlAlchemyAppointmentRepository = Depends(get_repo)):
    return repo.find_by_pet(pet_id)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: uuid.UUID, repo: SqlAlchemyAppointmentRepository = Depends(get_repo)):
    appointment = repo.find_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="La cita no existe")
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: uuid.UUID,
    data: AppointmentCreate,
    repo: SqlAlchemyAppointmentRepository = Depends(get_repo),
):
    appointment = repo.find_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="La cita no existe")
    appointment.pet_id = data.pet_id
    appointment.owner_id = data.owner_id
    appointment.date = data.date
    appointment.reason = data.reason
    appointment.cost = data.cost
    result = repo.update(appointment)
    return result


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def update_appointment_status(
    appointment_id: uuid.UUID,
    status: str,
    repo: SqlAlchemyAppointmentRepository = Depends(get_repo),
):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Use: {', '.join(VALID_STATUSES)}")
    result = repo.update_status(appointment_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="La cita no existe")
    return result


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: uuid.UUID, repo: SqlAlchemyAppointmentRepository = Depends(get_repo)):
    if not repo.delete(appointment_id):
        raise HTTPException(status_code=404, detail="La cita no existe")
    return {"message": "Cita eliminada"}
