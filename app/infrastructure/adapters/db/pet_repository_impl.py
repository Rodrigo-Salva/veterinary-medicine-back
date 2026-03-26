from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.entities.pet import Pet
from app.domain.ports.pet_repository import PetRepository
from app.infrastructure.adapters.db.models import PetModel


class SqlAlchemyPetRepository(PetRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, pm: PetModel) -> Pet:
        return Pet(
            id=pm.id,
            name=pm.name,
            species=pm.species,
            breed=pm.breed,
            age=pm.age,
            owner_id=pm.owner_id,
            medical_history=pm.medical_history,
            is_active=pm.is_active,
        )

    def save(self, pet: Pet) -> None:
        pet_model = PetModel(
            id=pet.id,
            name=pet.name,
            species=pet.species,
            breed=pet.breed,
            age=pet.age,
            owner_id=pet.owner_id,
            medical_history=pet.medical_history,
            is_active=pet.is_active,
        )
        self.db.add(pet_model)
        self.db.commit()

    def find_by_id(self, pet_id: uuid.UUID) -> Optional[Pet]:
        pm = self.db.query(PetModel).filter(PetModel.id == pet_id).first()
        return self._to_entity(pm) if pm else None

    def find_all(self) -> List[Pet]:
        return [self._to_entity(pm) for pm in self.db.query(PetModel).all()]

    def find_by_owner(self, owner_id: uuid.UUID) -> List[Pet]:
        return [
            self._to_entity(pm)
            for pm in self.db.query(PetModel).filter(PetModel.owner_id == owner_id).all()
        ]

    def update(self, pet_id: uuid.UUID, data: dict) -> Optional[Pet]:
        pm = self.db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not pm:
            return None
        for key, value in data.items():
            if hasattr(pm, key) and value is not None:
                setattr(pm, key, value)
        self.db.commit()
        self.db.refresh(pm)
        return self._to_entity(pm)

    def deactivate(self, pet_id: uuid.UUID) -> Optional[Pet]:
        pm = self.db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not pm:
            return None
        pm.is_active = False
        self.db.commit()
        self.db.refresh(pm)
        return self._to_entity(pm)
