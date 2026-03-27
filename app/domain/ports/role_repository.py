from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.role import Role, Permission


class RoleRepository(ABC):
    @abstractmethod
    def save(self, role: Role) -> Role:
        pass

    @abstractmethod
    def find_by_id(self, role_id: UUID) -> Optional[Role]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Role]:
        pass

    @abstractmethod
    def find_all(self) -> List[Role]:
        pass

    @abstractmethod
    def delete(self, role_id: UUID) -> bool:
        pass

    @abstractmethod
    def get_all_permissions(self) -> List[Permission]:
        pass

    @abstractmethod
    def set_role_permissions(self, role_id: UUID, permission_ids: List[UUID]) -> None:
        pass

    @abstractmethod
    def get_permissions_by_role_id(self, role_id: UUID) -> List[Permission]:
        pass
