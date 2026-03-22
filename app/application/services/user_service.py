from typing import Optional, List
from uuid import UUID
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.adapters.api.auth import get_password_hash, verify_password, create_access_token

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, email: str, password: str, role: str) -> User:
        hashed_password = get_password_hash(password)
        user = User.create(username, email, hashed_password, role)
        return self.user_repo.save(user)

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        user = self.user_repo.find_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        
        access_token = create_access_token(data={"sub": user.username, "role": user.role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.find_by_username(username)

    def get_all_users(self) -> List[User]:
        return self.user_repo.find_all()
