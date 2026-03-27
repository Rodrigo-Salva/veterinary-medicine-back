from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid
import os
import shutil
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.pet_repository_impl import SqlAlchemyPetRepository
<<<<<<< HEAD
from app.application.services.register_pet import RegisterPetUseCase
from app.infrastructure.adapters.api.schemas import PetCreate, PetUpdate, PetResponse
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/pets", tags=["pets"], dependencies=[Depends(get_current_user)])


def get_repo(db: Session = Depends(get_db)) -> SqlAlchemyPetRepository:
    return SqlAlchemyPetRepository(db)
=======
from app.infrastructure.adapters.api.schemas import PetCreate, PetResponse, PetUpdate, WeightRecordCreate, WeightRecordResponse
>>>>>>> b509e06 (refactor: enhance user and pet models with extended attributes)



@router.post("/", response_model=PetResponse)
<<<<<<< HEAD
def create_pet(pet_data: PetCreate, repo: SqlAlchemyPetRepository = Depends(get_repo)):
    use_case = RegisterPetUseCase(repo)
    return use_case.execute(
=======
def create_pet(pet_data: PetCreate, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    from app.domain.entities.pet import Pet
    pet = Pet(
        id=uuid.uuid4(),
>>>>>>> b509e06 (refactor: enhance user and pet models with extended attributes)
        name=pet_data.name,
        species=pet_data.species,
        breed=pet_data.breed,
        age=pet_data.age,
        owner_id=pet_data.owner_id,
<<<<<<< HEAD
    )


@router.get("/", response_model=List[PetResponse])
def list_pets(repo: SqlAlchemyPetRepository = Depends(get_repo)):
    return repo.find_all()
=======
        sex=pet_data.sex,
        color=pet_data.color,
        weight=pet_data.weight,
        allergies=pet_data.allergies,
        is_neutered=pet_data.is_neutered,
        microchip=pet_data.microchip,
        birth_date=pet_data.birth_date,
        notes=pet_data.notes,
    )
    saved = repository.save(pet)
    return saved


@router.get("/", response_model=List[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    return repository.find_all()
>>>>>>> b509e06 (refactor: enhance user and pet models with extended attributes)


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
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: uuid.UUID, data: PetUpdate, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    pet = repository.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    update_fields = data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(pet, field, value)
    saved = repository.save(pet)
    return saved


@router.patch("/{pet_id}/deactivate", response_model=PetResponse)
def toggle_pet_active(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    pet = repository.deactivate(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return pet


@router.post("/{pet_id}/photo", response_model=PetResponse)
def upload_pet_photo(pet_id: uuid.UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    pet = repository.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Save file
    upload_dir = os.path.join("uploads", "pets")
    os.makedirs(upload_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    filename = f"{pet_id}{ext}"
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    pet.photo_url = f"/uploads/pets/{filename}"
    saved = repository.save(pet)
    return saved


# ─── Weight Records ───────────────────────────────────────────────────────────

@router.post("/{pet_id}/weight", response_model=WeightRecordResponse)
def add_weight_record(pet_id: uuid.UUID, data: WeightRecordCreate, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    pet = repository.find_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    record = repository.add_weight_record(pet_id, data.weight, data.recorded_date, data.notes)
    return record


@router.get("/{pet_id}/weight", response_model=List[WeightRecordResponse])
def get_weight_history(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyPetRepository(db)
    return repository.get_weight_history(pet_id)
