from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from app.domain.entities.medical_record import MedicalRecord

class MedicalRecordRepository(ABC):
    @abstractmethod
    def save(self, record: MedicalRecord) -> MedicalRecord:
        pass

    @abstractmethod
    def find_by_pet_id(self, pet_id: uuid.UUID) -> List[MedicalRecord]:
        pass

    @abstractmethod
    def find_by_id(self, record_id: uuid.UUID) -> Optional[MedicalRecord]:
        pass
