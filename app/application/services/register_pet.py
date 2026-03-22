import uuid
from app.domain.entities.pet import Pet
from app.domain.ports.pet_repository import PetRepository

class RegisterPetUseCase:
    def __init__(self, pet_repository: PetRepository):
        self.pet_repository = pet_repository

    def execute(self, name: str, species: str, breed: str, age: int, owner_id: uuid.UUID) -> Pet:
        pet = Pet(
            id=uuid.uuid4(),
            name=name,
            species=species,
            breed=breed,
            age=age,
            owner_id=owner_id
        )
        self.pet_repository.save(pet)
        return pet
