from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from app.domain.entities.owner import Owner
from app.domain.ports.owner_repository import OwnerRepository
from app.infrastructure.adapters.db.models import OwnerModel

class SqlAlchemyOwnerRepository(OwnerRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, owner: Owner) -> None:
        owner_model = OwnerModel(
            id=owner.id,
            first_name=owner.first_name,
            last_name=owner.last_name,
            email=owner.email,
            phone=owner.phone
        )
        self.db.add(owner_model)
        self.db.commit()

    def find_by_id(self, owner_id: uuid.UUID) -> Optional[Owner]:
        owner_model = self.db.query(OwnerModel).filter(OwnerModel.id == owner_id).first()
        if owner_model:
            return Owner(
                id=owner_model.id,
                first_name=owner_model.first_name,
                last_name=owner_model.last_name,
                email=owner_model.email,
                phone=owner_model.phone
            )
        return None

    def find_all(self) -> List[Owner]:
        owner_models = self.db.query(OwnerModel).all()
        return [
            Owner(
                id=om.id,
                first_name=om.first_name,
                last_name=om.last_name,
                email=om.email,
                phone=om.phone
            ) for om in owner_models
        ]

    def find_by_email(self, email: str) -> Optional[Owner]:
        owner_model = self.db.query(OwnerModel).filter(OwnerModel.email == email).first()
        if owner_model:
            return Owner(
                id=owner_model.id,
                first_name=owner_model.first_name,
                last_name=owner_model.last_name,
                email=owner_model.email,
                phone=owner_model.phone
            )
        return None
