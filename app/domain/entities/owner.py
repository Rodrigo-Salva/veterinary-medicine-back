from dataclasses import dataclass
import uuid

@dataclass
class Owner:
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    phone: str
