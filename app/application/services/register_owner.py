import uuid
from app.domain.entities.owner import Owner
from app.domain.ports.owner_repository import OwnerRepository

class RegisterOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, first_name: str, last_name: str, email: str, phone: str) -> Owner:
        owner = Owner(
            id=uuid.uuid4(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        self.owner_repository.save(owner)
        return owner
