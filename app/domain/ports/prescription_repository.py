from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.prescription import Prescription

class PrescriptionRepository(ABC):
    @abstractmethod
    def save(self, prescription: Prescription) -> Prescription:
        pass

    @abstractmethod
    def find_by_pet(self, pet_id: UUID) -> List[Prescription]:
        pass

    @abstractmethod
    def find_by_id(self, prescription_id: UUID) -> Optional[Prescription]:
        pass

    @abstractmethod
    def delete(self, prescription_id: UUID) -> bool:
        pass
