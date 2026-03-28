from typing import List, Optional
import uuid
from datetime import date
from sqlalchemy.orm import Session, joinedload
from app.domain.entities.pet import Pet, WeightRecord
from app.domain.ports.pet_repository import PetRepository
from app.infrastructure.adapters.db.models import PetModel, WeightRecordModel



class SqlAlchemyPetRepository(PetRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, pet: Pet) -> Pet:
        existing = self.db.query(PetModel).filter(PetModel.id == pet.id).first()
        if existing:
            existing.name = pet.name
            existing.species = pet.species
            existing.breed = pet.breed
            existing.age = pet.age
            existing.owner_id = pet.owner_id
            existing.medical_history = pet.medical_history
            existing.is_active = pet.is_active
            existing.photo_url = pet.photo_url
            existing.sex = pet.sex
            existing.color = pet.color
            existing.weight = pet.weight
            existing.allergies = pet.allergies
            existing.is_neutered = pet.is_neutered
            existing.microchip = pet.microchip
            existing.birth_date = pet.birth_date
            existing.notes = pet.notes
        else:
            existing = PetModel(
                id=pet.id,
                name=pet.name,
                species=pet.species,
                breed=pet.breed,
                age=pet.age,
                owner_id=pet.owner_id,
                medical_history=pet.medical_history,
                is_active=pet.is_active,
                photo_url=pet.photo_url,
                sex=pet.sex,
                color=pet.color,
                weight=pet.weight,
                allergies=pet.allergies,
                is_neutered=pet.is_neutered,
                microchip=pet.microchip,
                birth_date=pet.birth_date,
                notes=pet.notes,
            )
            self.db.add(existing)
        self.db.commit()
        self.db.refresh(existing)
        return self._to_entity(existing)

    def find_by_id(self, pet_id: uuid.UUID) -> Optional[Pet]:
        model = (
            self.db.query(PetModel)
            .options(joinedload(PetModel.weight_records))
            .filter(PetModel.id == pet_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def find_all(self) -> List[Pet]:
        models = self.db.query(PetModel).all()
        return [self._to_entity(pm) for pm in models]

    def find_by_owner(self, owner_id: uuid.UUID) -> List[Pet]:
        models = self.db.query(PetModel).filter(PetModel.owner_id == owner_id).all()
        return [self._to_entity(pm) for pm in models]

    def update(self, pet: Pet) -> Pet:
        return self.save(pet)

    def deactivate(self, pet_id: uuid.UUID) -> Optional[Pet]:
        model = self.db.query(PetModel).filter(PetModel.id == pet_id).first()
        if not model:
            return None
        model.is_active = not model.is_active
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def add_weight_record(self, pet_id: uuid.UUID, weight: float, recorded_date: date, notes: Optional[str] = None) -> WeightRecord:
        record = WeightRecordModel(
            id=uuid.uuid4(),
            pet_id=pet_id,
            weight=weight,
            recorded_date=recorded_date,
            notes=notes,
        )
        self.db.add(record)
        pet_model = self.db.query(PetModel).filter(PetModel.id == pet_id).first()
        if pet_model:
            pet_model.weight = weight
        self.db.commit()
        return WeightRecord(id=record.id, pet_id=record.pet_id, weight=record.weight,
                            recorded_date=record.recorded_date, notes=record.notes)

    def get_weight_history(self, pet_id: uuid.UUID) -> List[WeightRecord]:
        models = (
            self.db.query(WeightRecordModel)
            .filter(WeightRecordModel.pet_id == pet_id)
            .order_by(WeightRecordModel.recorded_date.asc())
            .all()
        )
        return [
            WeightRecord(id=m.id, pet_id=m.pet_id, weight=m.weight,
                         recorded_date=m.recorded_date, notes=m.notes)
            for m in models
        ]

    def _to_entity(self, model: PetModel) -> Pet:
        weight_history = []
        if hasattr(model, 'weight_records') and model.weight_records:
            weight_history = [
                WeightRecord(id=wr.id, pet_id=wr.pet_id, weight=wr.weight,
                             recorded_date=wr.recorded_date, notes=wr.notes)
                for wr in model.weight_records
            ]
        return Pet(
            id=model.id,
            name=model.name,
            species=model.species,
            breed=model.breed,
            age=model.age,
            owner_id=model.owner_id,
            medical_history=model.medical_history,
            is_active=model.is_active if model.is_active is not None else True,
            photo_url=model.photo_url,
            sex=model.sex,
            color=model.color,
            weight=model.weight,
            allergies=model.allergies,
            is_neutered=model.is_neutered if model.is_neutered is not None else False,
            microchip=model.microchip,
            birth_date=model.birth_date,
            notes=model.notes,
            weight_history=weight_history,
        )
