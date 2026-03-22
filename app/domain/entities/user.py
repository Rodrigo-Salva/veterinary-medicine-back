from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class User:
    id: uuid.UUID
    username: str
    email: str
    hashed_password: str
    role: str  # "Admin", "Vet", "Receptionist"
    is_active: bool = True

    @classmethod
    def create(cls, username: str, email: str, hashed_password: str, role: str):
        return cls(
            id=uuid.uuid4(),
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_active=True
        )
