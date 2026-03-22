from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.owner_repository_impl import SqlAlchemyOwnerRepository
from app.application.services.register_owner import RegisterOwnerUseCase
from app.infrastructure.adapters.api.schemas import OwnerCreate, OwnerResponse

router = APIRouter(prefix="/owners", tags=["owners"])

@router.post("/", response_model=OwnerResponse)
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    repository = SqlAlchemyOwnerRepository(db)
    use_case = RegisterOwnerUseCase(repository)
    return use_case.execute(
        first_name=owner.first_name,
        last_name=owner.last_name,
        email=owner.email,
        phone=owner.phone
    )

@router.get("/", response_model=List[OwnerResponse])
def list_owners(db: Session = Depends(get_db)):
    repository = SqlAlchemyOwnerRepository(db)
    return repository.find_all()

@router.get("/{owner_id}", response_model=OwnerResponse)
def get_owner(owner_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = SqlAlchemyOwnerRepository(db)
    owner = repository.find_by_id(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner
