from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from datetime import datetime
from app.domain.entities.appointment import Appointment


class AppointmentRepository(ABC):
    @abstractmethod
    def save(self, appointment: Appointment) -> None:
        pass

    @abstractmethod
    def find_by_id(self, appointment_id: uuid.UUID) -> Optional[Appointment]:
        pass

    @abstractmethod
    def find_all(self) -> List[Appointment]:
        pass

    @abstractmethod
    def find_by_pet(self, pet_id: uuid.UUID) -> List[Appointment]:
        pass

    @abstractmethod
    def find_by_range(self, start: datetime, end: datetime) -> List[Appointment]:
        pass

    @abstractmethod
    def update(self, appointment: Appointment) -> Optional[Appointment]:
        pass

    @abstractmethod
    def update_status(self, appointment_id: uuid.UUID, status: str) -> Optional[Appointment]:
        pass

    @abstractmethod
    def delete(self, appointment_id: uuid.UUID) -> bool:
        pass
