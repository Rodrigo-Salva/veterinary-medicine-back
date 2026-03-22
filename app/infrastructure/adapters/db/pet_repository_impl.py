from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.entities.pet import Pet
from app.domain.ports.pet_repository import PetRepository
from app.infrastructure.adapters.db.models import PetModel

class SqlAlchemyPetRepository(PetRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, pet: Pet) -> None:
        pet_model = PetModel(
            id=pet.id,
            name=pet.name,
            species=pet.species,
            breed=pet.breed,
            age=pet.age,
            owner_id=pet.owner_id,
            medical_history=pet.medical_history
        )
        self.db.add(pet_model)
        self.db.commit()

    def find_by_id(self, pet_id: uuid.UUID) -> Optional[Pet]:
        pet_model = self.db.query(PetModel).filter(PetModel.id == pet_id).first()
        if pet_model:
            return Pet(
                id=pet_model.id,
                name=pet_model.name,
                species=pet_model.species,
                breed=pet_model.breed,
                age=pet_model.age,
                owner_id=pet_model.owner_id,
                medical_history=pet_model.medical_history
            )
        return None

    def find_all(self) -> List[Pet]:
        pet_models = self.db.query(PetModel).all()
        return [
            Pet(
                id=pm.id,
                name=pm.name,
                species=pm.species,
                breed=pm.breed,
                age=pm.age,
                owner_id=pm.owner_id,
                medical_history=pm.medical_history
            ) for pm in pet_models
        ]

    def find_by_owner(self, owner_id: uuid.UUID) -> List[Pet]:
        pet_models = self.db.query(PetModel).filter(PetModel.owner_id == owner_id).all()
        return [
            Pet(
                id=pm.id,
                name=pm.name,
                species=pm.species,
                breed=pm.breed,
                age=pm.age,
                owner_id=pm.owner_id,
                medical_history=pm.medical_history
            ) for pm in pet_models
        ]
