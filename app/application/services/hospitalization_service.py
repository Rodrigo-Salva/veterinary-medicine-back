from app.domain.entities.hospitalization import Hospitalization, VitalSignRecord
from app.domain.ports.hospitalization_repository import HospitalizationRepository
import uuid
from datetime import datetime
from typing import Optional

class HospitalizationUseCase:
    def __init__(self, repository: HospitalizationRepository):
        self.repository = repository

    def check_in(self, pet_id: uuid.UUID, cage_id: uuid.UUID, reason: str) -> Hospitalization:
        cage = self.repository.get_cage_by_id(cage_id)
        if not cage or cage.is_occupied:
            raise Exception("Cage not available")

        # Update cage status
        cage.is_occupied = True
        cage.current_pet_id = pet_id
        self.repository.save_cage(cage)

        # Create hospitalization record
        hospitalization = Hospitalization(
            id=uuid.uuid4(),
            pet_id=pet_id,
            cage_id=cage_id,
            check_in_date=datetime.utcnow(),
            reason=reason
        )
        return self.repository.save_hospitalization(hospitalization)

    def record_vitals(self, hospitalization_id: uuid.UUID, temperature: float, heart_rate: int, respiratory_rate: int, notes: str) -> VitalSignRecord:
        record = VitalSignRecord(
            id=uuid.uuid4(),
            hospitalization_id=hospitalization_id,
            timestamp=datetime.utcnow(),
            temperature=temperature,
            heart_rate=heart_rate,
            respiratory_rate=respiratory_rate,
            notes=notes
        )
        return self.repository.save_vital_sign(record)

    def discharge(self, hospitalization_id: uuid.UUID) -> Hospitalization:
        hosp = self.repository.get_hospitalization_by_id(hospitalization_id)
        if not hosp or hosp.status != "Active":
            raise Exception("Active hospitalization not found")

        hosp.status = "Discharged"
        hosp.check_out_date = datetime.utcnow()
        self.repository.save_hospitalization(hosp)

        # Free the cage
        cage = self.repository.get_cage_by_id(hosp.cage_id)
        if cage:
            cage.is_occupied = False
            cage.current_pet_id = None
            self.repository.save_cage(cage)
            
        return hosp
