from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.pet_repository_impl import SqlAlchemyPetRepository
from app.application.services.register_pet import RegisterPetUseCase
from app.infrastructure.adapters.api.schemas import PetCreate, PetResponse

router = APIRouter(prefix="/pets", tags=["pets"])

@router.post("/", response_model=PetResponse)
def create_pet(pet_data: PetCreate, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    use_case = RegisterPetUseCase(repository)
    
    pet = use_case.execute(
        name=pet_data.name,
        species=pet_data.species,
        breed=pet_data.breed,
        age=pet_data.age,
        owner_id=pet_data.owner_id
    )
    return pet

@router.get("/", response_model=List[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    pets = repository.find_all()
    return pets

@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    pet = repository.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet
