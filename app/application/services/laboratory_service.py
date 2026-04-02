from typing import List
import uuid
from datetime import datetime
from app.domain.entities.laboratory import LaboratoryResult
from app.domain.ports.laboratory_repository import LaboratoryRepository

class LaboratoryService:
    def __init__(self, repository: LaboratoryRepository):
        self.repository = repository

    def add_result(
        self,
        pet_id: uuid.UUID,
        test_name: str,
        category: str,
        notes: str = None,
        parameters: str = None
    ) -> LaboratoryResult:
        result = LaboratoryResult(
            id=uuid.uuid4(),
            pet_id=pet_id,
            test_name=test_name,
            category=category,
            result_date=datetime.utcnow(),
            notes=notes,
            parameters=parameters
        )
        return self.repository.save(result)

    def get_pet_results(self, pet_id: uuid.UUID) -> List[LaboratoryResult]:
        return self.repository.get_by_pet(pet_id)

    def delete_result(self, id: uuid.UUID) -> bool:
        return self.repository.delete(id)
