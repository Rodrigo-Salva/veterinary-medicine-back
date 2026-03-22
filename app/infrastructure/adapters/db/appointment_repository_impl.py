from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.entities.appointment import Appointment
from app.domain.ports.appointment_repository import AppointmentRepository
from app.infrastructure.adapters.db.models import AppointmentModel

class SqlAlchemyAppointmentRepository(AppointmentRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, appointment: Appointment) -> None:
        appointment_model = AppointmentModel(
            id=appointment.id,
            pet_id=appointment.pet_id,
            owner_id=appointment.owner_id,
            date=appointment.date,
            reason=appointment.reason,
            status=appointment.status,
            cost=appointment.cost
        )
        self.db.add(appointment_model)
        self.db.commit()

    def find_by_id(self, appointment_id: uuid.UUID) -> Optional[Appointment]:
        am = self.db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
        if am:
            return Appointment(
                id=am.id,
                pet_id=am.pet_id,
                owner_id=am.owner_id,
                date=am.date,
                reason=am.reason,
                status=am.status,
                cost=am.cost
            )
        return None

    def find_all(self) -> List[Appointment]:
        ams = self.db.query(AppointmentModel).all()
        return [
            Appointment(
                id=am.id,
                pet_id=am.pet_id,
                owner_id=am.owner_id,
                date=am.date,
                reason=am.reason,
                status=am.status,
                cost=am.cost
            ) for am in ams
        ]

    def find_by_pet(self, pet_id: uuid.UUID) -> List[Appointment]:
        ams = self.db.query(AppointmentModel).filter(AppointmentModel.pet_id == pet_id).all()
        return [
            Appointment(
                id=am.id,
                pet_id=am.pet_id,
                owner_id=am.owner_id,
                date=am.date,
                reason=am.reason,
                status=am.status,
                cost=am.cost
            ) for am in ams
        ]
