from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.pet_repository_impl import SqlAlchemyPetRepository
from app.application.services.register_pet import RegisterPetUseCase
from app.infrastructure.adapters.api.schemas import PetCreate, PetUpdate, PetResponse
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/pets", tags=["pets"], dependencies=[Depends(get_current_user)])


def get_repo(db: Session = Depends(get_db)) -> SqlAlchemyPetRepository:
    return SqlAlchemyPetRepository(db)


@router.post("/", response_model=PetResponse)
def create_pet(pet_data: PetCreate, repo: SqlAlchemyPetRepository = Depends(get_repo)):
    use_case = RegisterPetUseCase(repo)
    return use_case.execute(
        name=pet_data.name,
        species=pet_data.species,
        breed=pet_data.breed,
        age=pet_data.age,
        owner_id=pet_data.owner_id,
    )


@router.get("/", response_model=List[PetResponse])
def list_pets(repo: SqlAlchemyPetRepository = Depends(get_repo)):
    return repo.find_all()


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: uuid.UUID, repo: SqlAlchemyPetRepository = Depends(get_repo)):
    pet = repo.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: uuid.UUID, pet_data: PetUpdate, repo: SqlAlchemyPetRepository = Depends(get_repo)):
    pet = repo.update(pet_id, pet_data.model_dump(exclude_none=True))
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.patch("/{pet_id}/deactivate", response_model=PetResponse)
def deactivate_pet(pet_id: uuid.UUID, repo: SqlAlchemyPetRepository = Depends(get_repo)):
    pet = repo.deactivate(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet
