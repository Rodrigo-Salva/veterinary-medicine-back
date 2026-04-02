from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.laboratory_repository_impl import SqlAlchemyLaboratoryRepository
from app.application.services.laboratory_service import LaboratoryService
from app.infrastructure.adapters.api.schemas_laboratory import (
    LaboratoryResultCreate, LaboratoryResultResponse
)
from app.infrastructure.adapters.api.auth import permission_required

router = APIRouter(prefix="/laboratory", tags=["laboratory"])

def get_laboratory_service(db: Session = Depends(get_db)):
    return LaboratoryService(SqlAlchemyLaboratoryRepository(db))

@router.get("/pet/{pet_id}", response_model=List[LaboratoryResultResponse])
def get_pet_lab_results(
    pet_id: UUID,
    service: LaboratoryService = Depends(get_laboratory_service),
    _=Depends(permission_required("laboratorio", "listar")),
):
    return service.get_pet_results(pet_id)

@router.post("/", response_model=LaboratoryResultResponse, status_code=status.HTTP_201_CREATED)
def add_lab_result(
    data: LaboratoryResultCreate,
    service: LaboratoryService = Depends(get_laboratory_service),
    _=Depends(permission_required("laboratorio", "registrar")),
):
    return service.add_result(
        pet_id=data.pet_id,
        test_name=data.test_name,
        category=data.category,
        notes=data.notes,
        parameters=data.parameters
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lab_result(
    id: UUID,
    service: LaboratoryService = Depends(get_laboratory_service),
    _=Depends(permission_required("laboratorio", "eliminar")),
):
    if not service.delete_result(id):
        raise HTTPException(status_code=404, detail="Resultado de laboratorio no encontrado")
