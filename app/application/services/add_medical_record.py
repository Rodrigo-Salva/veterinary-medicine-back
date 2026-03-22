from app.domain.entities.medical_record import MedicalRecord
from app.domain.ports.medical_record_repository import MedicalRecordRepository
import uuid
from datetime import datetime

class AddMedicalRecordUseCase:
    def __init__(self, repository: MedicalRecordRepository):
        self.repository = repository

    def execute(self, pet_id: uuid.UUID, description: str, diagnosis: str, treatment: str) -> MedicalRecord:
        record = MedicalRecord(
            id=uuid.uuid4(),
            pet_id=pet_id,
            recording_date=datetime.utcnow(),
            description=description,
            diagnosis=diagnosis,
            treatment=treatment
        )
        return self.repository.save(record)
