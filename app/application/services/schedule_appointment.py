import uuid
from datetime import datetime
from app.domain.entities.appointment import Appointment
from app.domain.ports.appointment_repository import AppointmentRepository

class ScheduleAppointmentUseCase:
    def __init__(self, appointment_repository: AppointmentRepository):
        self.appointment_repository = appointment_repository

    def execute(self, pet_id: uuid.UUID, owner_id: uuid.UUID, date: datetime, reason: str, cost: float) -> Appointment:
        appointment = Appointment(
            id=uuid.uuid4(),
            pet_id=pet_id,
            owner_id=owner_id,
            date=date,
            reason=reason,
            status="Pending",
            cost=cost
        )
        self.appointment_repository.save(appointment)
        return appointment
