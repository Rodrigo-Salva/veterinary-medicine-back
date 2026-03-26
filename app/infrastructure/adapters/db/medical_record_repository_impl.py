from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.domain.entities.medical_record import MedicalRecord
from app.domain.ports.medical_record_repository import MedicalRecordRepository
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel

class SqlAlchemyMedicalRecordRepository(MedicalRecordRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, record: MedicalRecord) -> MedicalRecord:
        db_record = MedicalRecordModel(
            id=record.id,
            pet_id=record.pet_id,
            recording_date=record.recording_date,
            description=record.description,
            diagnosis=record.diagnosis,
            treatment=record.treatment,
            record_type=record.record_type,
            next_date=record.next_date,
            vet_id=record.vet_id,
        )
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return self._to_entity(db_record)

    def find_by_pet_id(self, pet_id: uuid.UUID) -> List[MedicalRecord]:
        db_records = self.db.query(MedicalRecordModel).filter(MedicalRecordModel.pet_id == pet_id).all()
        return [self._to_entity(r) for r in db_records]

    def find_by_id(self, record_id: uuid.UUID) -> Optional[MedicalRecord]:
        db_record = self.db.query(MedicalRecordModel).filter(MedicalRecordModel.id == record_id).first()
        return self._to_entity(db_record) if db_record else None

    def _to_entity(self, db_record: MedicalRecordModel) -> MedicalRecord:
        return MedicalRecord(
            id=db_record.id,
            pet_id=db_record.pet_id,
            recording_date=db_record.recording_date,
            description=db_record.description,
            diagnosis=db_record.diagnosis,
            treatment=db_record.treatment,
            record_type=db_record.record_type or "Consultation",
            next_date=db_record.next_date,
            vet_id=db_record.vet_id,
        )
