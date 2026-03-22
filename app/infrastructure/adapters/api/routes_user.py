from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.user_repository_impl import SqlAlchemyUserRepository
from app.application.services.user_service import UserService
from app.infrastructure.adapters.api.schemas_user import LoginRequest, Token, UserResponse, UserCreate
from app.infrastructure.adapters.api.auth import get_current_user, role_required
from app.domain.entities.user import User
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)):
    user_repo = SqlAlchemyUserRepository(db)
    return UserService(user_repo)

@router.post("/login", response_model=Token)
def login(request: LoginRequest, user_service: UserService = Depends(get_user_service)):
    result = user_service.authenticate_user(request.username, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    user_service: UserService = Depends(get_user_service),
    admin_user: User = Depends(role_required(["Admin"]))
):
    return user_service.get_all_users()

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate, 
    user_service: UserService = Depends(get_user_service),
    admin_user: User = Depends(role_required(["Admin"]))
):
    return user_service.register_user(
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role
    )
