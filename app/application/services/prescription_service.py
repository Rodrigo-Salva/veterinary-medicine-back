from typing import List, Optional
from uuid import UUID
from app.domain.entities.prescription import Prescription
from app.domain.ports.prescription_repository import PrescriptionRepository

class PrescriptionUseCase:
    def __init__(self, repository: PrescriptionRepository):
        self.repository = repository

    def create_prescription(self, pet_id: UUID, medications: str, instructions: str, medical_record_id: Optional[UUID] = None) -> Prescription:
        prescription = Prescription.create(
            pet_id=pet_id,
            medications=medications,
            instructions=instructions,
            medical_record_id=medical_record_id
        )
        return self.repository.save(prescription)

    def get_pet_prescriptions(self, pet_id: UUID) -> List[Prescription]:
        return self.repository.find_by_pet(pet_id)

    def get_prescription(self, prescription_id: UUID) -> Optional[Prescription]:
        return self.repository.find_by_id(prescription_id)

    def delete_prescription(self, prescription_id: UUID) -> bool:
        return self.repository.delete(prescription_id)
