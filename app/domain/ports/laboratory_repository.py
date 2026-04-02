from abc import ABC, abstractmethod
from typing import List
import uuid
from app.domain.entities.laboratory import LaboratoryResult

class LaboratoryRepository(ABC):
    @abstractmethod
    def save(self, result: LaboratoryResult) -> LaboratoryResult:
        pass

    @abstractmethod
    def get_by_pet(self, pet_id: uuid.UUID) -> List[LaboratoryResult]:
        pass

    @abstractmethod
    def delete(self, id: uuid.UUID) -> bool:
        pass
