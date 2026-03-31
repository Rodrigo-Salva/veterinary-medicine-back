from dataclasses import dataclass, field
from typing import Optional, List
import uuid


@dataclass
class Permission:
    id: uuid.UUID
    module: str
    action: str


@dataclass
class Role:
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    is_active: bool = True
    permissions: List[Permission] = field(default_factory=list)

    @classmethod
    def create(cls, name: str, description: Optional[str] = None):
        return cls(
            id=uuid.uuid4(),
            name=name,
            description=description,
            is_active=True,
            permissions=[],
        )
