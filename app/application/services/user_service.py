from typing import Optional, List
from uuid import UUID
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.adapters.api.auth import get_password_hash, verify_password, create_access_token


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, email: str, password: str, role_id: UUID) -> User:
        hashed_password = get_password_hash(password)
        user = User.create(username, email, hashed_password, role_id)
        return self.user_repo.save(user)

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        user = self.user_repo.find_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        access_token = create_access_token(data={"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "email": user.email,
                "role_id": str(user.role_id),
                "role_name": user.role_name,
                "is_active": user.is_active,
                "permissions": user.permissions or [],
            },
        }

    def update_user(self, user_id: UUID, username: str = None, email: str = None,
                     password: str = None, role_id: UUID = None) -> Optional[User]:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.hashed_password = get_password_hash(password)
        if role_id:
            user.role_id = role_id
        return self.user_repo.save(user)

    def toggle_user_active(self, user_id: UUID) -> Optional[User]:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return None
        user.is_active = not user.is_active
        return self.user_repo.save(user)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.find_by_username(username)

    def get_all_users(self) -> List[User]:
        return self.user_repo.find_all()
