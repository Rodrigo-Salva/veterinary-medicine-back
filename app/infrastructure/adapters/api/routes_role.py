from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.role_repository_impl import SqlAlchemyRoleRepository
from app.application.services.role_service import RoleService
from app.infrastructure.adapters.api.schemas_role import (
    RoleCreate, RoleUpdate, RoleResponse, PermissionResponse, SetPermissionsRequest,
)
from app.infrastructure.adapters.api.auth import permission_required

router = APIRouter(prefix="/roles", tags=["roles"])


def get_role_service(db: Session = Depends(get_db)):
    return RoleService(SqlAlchemyRoleRepository(db))


@router.get("/", response_model=List[RoleResponse])
def get_all_roles(
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "listar")),
):
    roles = role_service.get_all_roles()
    return [
        RoleResponse(
            id=r.id, name=r.name, description=r.description, is_active=r.is_active,
            permissions=[PermissionResponse(id=p.id, module=p.module, action=p.action) for p in r.permissions],
        )
        for r in roles
    ]


@router.get("/permissions", response_model=List[PermissionResponse])
def get_all_permissions(
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "listar")),
):
    return role_service.get_all_permissions()


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "listar")),
):
    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return RoleResponse(
        id=role.id, name=role.name, description=role.description, is_active=role.is_active,
        permissions=[PermissionResponse(id=p.id, module=p.module, action=p.action) for p in role.permissions],
    )


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    data: RoleCreate,
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "registrar")),
):
    try:
        role = role_service.create_role(name=data.name, description=data.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return RoleResponse(
        id=role.id, name=role.name, description=role.description, is_active=role.is_active,
        permissions=[],
    )


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: UUID,
    data: RoleUpdate,
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "editar")),
):
    role = role_service.update_role(role_id, name=data.name, description=data.description)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return RoleResponse(
        id=role.id, name=role.name, description=role.description, is_active=role.is_active,
        permissions=[PermissionResponse(id=p.id, module=p.module, action=p.action) for p in role.permissions],
    )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: UUID,
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "eliminar")),
):
    if not role_service.delete_role(role_id):
        raise HTTPException(status_code=404, detail="Rol no encontrado")


@router.put("/{role_id}/permissions", response_model=RoleResponse)
def set_role_permissions(
    role_id: UUID,
    data: SetPermissionsRequest,
    role_service: RoleService = Depends(get_role_service),
    _=Depends(permission_required("roles", "editar")),
):
    try:
        role = role_service.set_role_permissions(role_id, data.permission_ids)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return RoleResponse(
        id=role.id, name=role.name, description=role.description, is_active=role.is_active,
        permissions=[PermissionResponse(id=p.id, module=p.module, action=p.action) for p in role.permissions],
    )
