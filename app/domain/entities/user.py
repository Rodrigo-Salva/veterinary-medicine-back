from dataclasses import dataclass, field
from typing import Optional, List
import uuid


@dataclass
class User:
    id: uuid.UUID
    username: str
    email: str
    hashed_password: str
    role_id: uuid.UUID
    is_active: bool = True
    role_name: Optional[str] = None
    permissions: List[dict] = field(default_factory=list)

    @classmethod
    def create(cls, username: str, email: str, hashed_password: str, role_id: uuid.UUID):
        return cls(
            id=uuid.uuid4(),
            username=username,
            email=email,
            hashed_password=hashed_password,
            role_id=role_id,
            is_active=True,
        )
