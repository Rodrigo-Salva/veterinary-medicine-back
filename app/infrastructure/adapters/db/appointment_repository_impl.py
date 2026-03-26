from typing import List, Optional
import uuid
from datetime import datetime
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
        return self._to_entity(am) if am else None

    def find_all(self) -> List[Appointment]:
        ams = self.db.query(AppointmentModel).all()
        return [self._to_entity(am) for am in ams]

    def find_by_pet(self, pet_id: uuid.UUID) -> List[Appointment]:
        ams = self.db.query(AppointmentModel).filter(AppointmentModel.pet_id == pet_id).all()
        return [self._to_entity(am) for am in ams]

    def find_by_range(self, start: datetime, end: datetime) -> List[Appointment]:
        ams = (
            self.db.query(AppointmentModel)
            .filter(AppointmentModel.date >= start, AppointmentModel.date <= end)
            .order_by(AppointmentModel.date)
            .all()
        )
        return [self._to_entity(am) for am in ams]

    def update(self, appointment: Appointment) -> Optional[Appointment]:
        am = self.db.query(AppointmentModel).filter(AppointmentModel.id == appointment.id).first()
        if not am:
            return None
        am.pet_id = appointment.pet_id
        am.owner_id = appointment.owner_id
        am.date = appointment.date
        am.reason = appointment.reason
        am.cost = appointment.cost
        self.db.commit()
        self.db.refresh(am)
        return self._to_entity(am)

    def update_status(self, appointment_id: uuid.UUID, status: str) -> Optional[Appointment]:
        am = self.db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
        if not am:
            return None
        am.status = status
        self.db.commit()
        self.db.refresh(am)
        return self._to_entity(am)

    def delete(self, appointment_id: uuid.UUID) -> bool:
        am = self.db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
        if not am:
            return False
        self.db.delete(am)
        self.db.commit()
        return True

    def _to_entity(self, am: AppointmentModel) -> Appointment:
        return Appointment(
            id=am.id,
            pet_id=am.pet_id,
            owner_id=am.owner_id,
            date=am.date,
            reason=am.reason,
            status=am.status,
            cost=am.cost,
        )
