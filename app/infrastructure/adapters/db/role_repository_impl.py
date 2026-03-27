from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID
import uuid

from app.domain.entities.role import Role, Permission
from app.domain.ports.role_repository import RoleRepository
from app.infrastructure.adapters.db.models_role import RoleModel, PermissionModel, RolePermissionModel


class SqlAlchemyRoleRepository(RoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, role: Role) -> Role:
        model = self.db.query(RoleModel).filter(RoleModel.id == role.id).first()
        if model:
            model.name = role.name
            model.description = role.description
            model.is_active = role.is_active
        else:
            model = RoleModel(
                id=role.id,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
            )
            self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def find_by_id(self, role_id: UUID) -> Optional[Role]:
        model = (
            self.db.query(RoleModel)
            .options(joinedload(RoleModel.permissions).joinedload(RolePermissionModel.permission))
            .filter(RoleModel.id == role_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def find_by_name(self, name: str) -> Optional[Role]:
        model = (
            self.db.query(RoleModel)
            .options(joinedload(RoleModel.permissions).joinedload(RolePermissionModel.permission))
            .filter(RoleModel.name == name)
            .first()
        )
        return self._to_entity(model) if model else None

    def find_all(self) -> List[Role]:
        models = (
            self.db.query(RoleModel)
            .options(joinedload(RoleModel.permissions).joinedload(RolePermissionModel.permission))
            .all()
        )
        return [self._to_entity(m) for m in models]

    def delete(self, role_id: UUID) -> bool:
        model = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def get_all_permissions(self) -> List[Permission]:
        models = self.db.query(PermissionModel).order_by(PermissionModel.module, PermissionModel.action).all()
        return [Permission(id=m.id, module=m.module, action=m.action) for m in models]

    def set_role_permissions(self, role_id: UUID, permission_ids: List[UUID]) -> None:
        self.db.query(RolePermissionModel).filter(RolePermissionModel.role_id == role_id).delete()
        for pid in permission_ids:
            rp = RolePermissionModel(id=uuid.uuid4(), role_id=role_id, permission_id=pid)
            self.db.add(rp)
        self.db.commit()

    def get_permissions_by_role_id(self, role_id: UUID) -> List[Permission]:
        results = (
            self.db.query(PermissionModel)
            .join(RolePermissionModel, RolePermissionModel.permission_id == PermissionModel.id)
            .filter(RolePermissionModel.role_id == role_id)
            .all()
        )
        return [Permission(id=m.id, module=m.module, action=m.action) for m in results]

    def _to_entity(self, model: RoleModel) -> Role:
        permissions = []
        for rp in model.permissions:
            p = rp.permission
            permissions.append(Permission(id=p.id, module=p.module, action=p.action))
        return Role(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            permissions=permissions,
        )
