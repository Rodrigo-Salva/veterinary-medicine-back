from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from app.domain.entities.pet import Pet

class PetRepository(ABC):
    @abstractmethod
    def save(self, pet: Pet) -> None:
        pass

    @abstractmethod
    def find_by_id(self, pet_id: uuid.UUID) -> Optional[Pet]:
        pass

    @abstractmethod
    def find_all(self) -> List[Pet]:
        pass

    @abstractmethod
    def find_by_owner(self, owner_id: uuid.UUID) -> List[Pet]:
        pass

    @abstractmethod
    def update(self, pet_id: uuid.UUID, data: dict) -> Optional[Pet]:
        pass

    @abstractmethod
    def deactivate(self, pet_id: uuid.UUID) -> Optional[Pet]:
        pass
