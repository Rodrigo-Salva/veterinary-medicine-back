from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.adapters.db.models_user import UserModel

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        user_model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if user_model:
            user_model.username = user.username
            user_model.email = user.email
            user_model.hashed_password = user.hashed_password
            user_model.role = user.role
            user_model.is_active = user.is_active
        else:
            user_model = UserModel(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                role=user.role,
                is_active=user.is_active
            )
            self.db.add(user_model)
        
        self.db.commit()
        return user

    def find_by_username(self, username: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(model) if model else None

    def find_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def find_all(self) -> List[User]:
        models = self.db.query(UserModel).all()
        return [self._to_entity(m) for m in models]

    def delete(self, user_id: UUID) -> bool:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            role=model.role,
            is_active=model.is_active
        )
