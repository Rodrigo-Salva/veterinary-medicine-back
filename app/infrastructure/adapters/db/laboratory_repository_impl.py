from sqlalchemy.orm import Session
from typing import List
import uuid
from app.domain.entities.laboratory import LaboratoryResult
from app.domain.ports.laboratory_repository import LaboratoryRepository
from app.infrastructure.adapters.db.models_medical import LaboratoryResultModel

class SqlAlchemyLaboratoryRepository: # Use this name directly in the service
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: LaboratoryResult) -> LaboratoryResult:
        model = LaboratoryResultModel(
            id=entity.id,
            pet_id=entity.pet_id,
            test_name=entity.test_name,
            category=entity.category,
            result_date=entity.result_date,
            notes=entity.notes,
            parameters=entity.parameters
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return LaboratoryResult(
            id=model.id,
            pet_id=model.pet_id,
            test_name=model.test_name,
            category=model.category,
            result_date=model.result_date,
            notes=model.notes,
            parameters=model.parameters
        )

    def get_by_pet(self, pet_id: uuid.UUID) -> List[LaboratoryResult]:
        models = self.db.query(LaboratoryResultModel).filter(LaboratoryResultModel.pet_id == pet_id).all()
        return [
            LaboratoryResult(
                id=m.id,
                pet_id=m.pet_id,
                test_name=m.test_name,
                category=m.category,
                result_date=m.result_date,
                notes=m.notes,
                parameters=m.parameters
            )
            for m in models
        ]

    def delete(self, id: uuid.UUID) -> bool:
        model = self.db.query(LaboratoryResultModel).filter(LaboratoryResultModel.id == id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False
