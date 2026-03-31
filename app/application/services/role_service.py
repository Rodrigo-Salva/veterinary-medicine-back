from typing import List, Optional
from uuid import UUID
from app.domain.entities.role import Role, Permission
from app.domain.ports.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def create_role(self, name: str, description: Optional[str] = None) -> Role:
        existing = self.role_repo.find_by_name(name)
        if existing:
            raise ValueError(f"El rol '{name}' ya existe")
        role = Role.create(name=name, description=description)
        return self.role_repo.save(role)

    def update_role(self, role_id: UUID, name: str, description: Optional[str] = None) -> Optional[Role]:
        role = self.role_repo.find_by_id(role_id)
        if not role:
            return None
        role.name = name
        role.description = description
        return self.role_repo.save(role)

    def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        return self.role_repo.find_by_id(role_id)

    def get_all_roles(self) -> List[Role]:
        return self.role_repo.find_all()

    def delete_role(self, role_id: UUID) -> bool:
        return self.role_repo.delete(role_id)

    def get_all_permissions(self) -> List[Permission]:
        return self.role_repo.get_all_permissions()

    def set_role_permissions(self, role_id: UUID, permission_ids: List[UUID]) -> Role:
        role = self.role_repo.find_by_id(role_id)
        if not role:
            raise ValueError("Rol no encontrado")
        self.role_repo.set_role_permissions(role_id, permission_ids)
        return self.role_repo.find_by_id(role_id)

    def get_permissions_by_role_id(self, role_id: UUID) -> List[Permission]:
        return self.role_repo.get_permissions_by_role_id(role_id)
