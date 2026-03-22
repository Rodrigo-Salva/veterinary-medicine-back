from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.prescription import Prescription
from app.domain.ports.prescription_repository import PrescriptionRepository
from app.infrastructure.adapters.db.models_medical import PrescriptionModel

class SqlAlchemyPrescriptionRepository(PrescriptionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, prescription: Prescription) -> Prescription:
        model = PrescriptionModel(
            id=prescription.id,
            pet_id=prescription.pet_id,
            medical_record_id=prescription.medical_record_id,
            date=prescription.date,
            medications=prescription.medications,
            instructions=prescription.instructions
        )
        self.db.add(model)
        self.db.commit()
        return self._to_entity(model)

    def find_by_pet(self, pet_id: UUID) -> List[Prescription]:
        models = self.db.query(PrescriptionModel).filter(PrescriptionModel.pet_id == pet_id).all()
        return [self._to_entity(m) for m in models]

    def find_by_id(self, prescription_id: UUID) -> Optional[Prescription]:
        model = self.db.query(PrescriptionModel).filter(PrescriptionModel.id == prescription_id).first()
        return self._to_entity(model) if model else None

    def delete(self, prescription_id: UUID) -> bool:
        model = self.db.query(PrescriptionModel).filter(PrescriptionModel.id == prescription_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def _to_entity(self, model: PrescriptionModel) -> Prescription:
        return Prescription(
            id=model.id,
            pet_id=model.pet_id,
            medical_record_id=model.medical_record_id,
            date=model.date,
            medications=model.medications,
            instructions=model.instructions
        )
