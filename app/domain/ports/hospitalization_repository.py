from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from app.domain.entities.hospitalization import Hospitalization, Cage, VitalSignRecord

class HospitalizationRepository(ABC):
    @abstractmethod
    def save_cage(self, cage: Cage) -> Cage:
        pass

    @abstractmethod
    def get_cages(self) -> List[Cage]:
        pass

    @abstractmethod
    def get_cage_by_id(self, cage_id: uuid.UUID) -> Optional[Cage]:
        pass

    @abstractmethod
    def save_hospitalization(self, hospitalization: Hospitalization) -> Hospitalization:
        pass

    @abstractmethod
    def get_hospitalization_by_id(self, hosp_id: uuid.UUID) -> Optional[Hospitalization]:
        pass

    @abstractmethod
    def get_active_hospitalization_by_pet_id(self, pet_id: uuid.UUID) -> Optional[Hospitalization]:
        pass

    @abstractmethod
    def save_vital_sign(self, record: VitalSignRecord) -> VitalSignRecord:
        pass
        
    @abstractmethod
    def get_vital_signs_by_hosp_id(self, hosp_id: uuid.UUID) -> List[VitalSignRecord]:
        pass
