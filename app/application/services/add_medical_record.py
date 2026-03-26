from app.domain.entities.medical_record import MedicalRecord
from app.domain.ports.medical_record_repository import MedicalRecordRepository
import uuid
from datetime import datetime

class AddMedicalRecordUseCase:
    def __init__(self, repository: MedicalRecordRepository):
        self.repository = repository

    def execute(
        self,
        pet_id: uuid.UUID,
        description: str,
        diagnosis: str,
        treatment: str,
        record_type: str = "Consultation",
        next_date=None,
        vet_id: uuid.UUID = None,
    ) -> MedicalRecord:
        record = MedicalRecord(
            id=uuid.uuid4(),
            pet_id=pet_id,
            recording_date=datetime.utcnow(),
            description=description,
            diagnosis=diagnosis,
            treatment=treatment,
            record_type=record_type,
            next_date=next_date,
            vet_id=vet_id,
        )
        return self.repository.save(record)
