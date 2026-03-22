from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from app.domain.entities.owner import Owner

class OwnerRepository(ABC):
    @abstractmethod
    def save(self, owner: Owner) -> None:
        pass

    @abstractmethod
    def find_by_id(self, owner_id: uuid.UUID) -> Optional[Owner]:
        pass

    @abstractmethod
    def find_all(self) -> List[Owner]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Owner]:
        pass
