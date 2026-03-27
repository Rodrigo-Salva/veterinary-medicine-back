from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uuid


class PermissionItem(BaseModel):
    module: str
    action: str


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role_id: uuid.UUID
    role_name: Optional[str] = None
    is_active: bool = True
    permissions: List[PermissionItem] = []


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: uuid.UUID


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[uuid.UUID] = None


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    role_id: uuid.UUID
    role_name: Optional[str] = None
    is_active: bool
    permissions: List[PermissionItem] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserBase


class LoginRequest(BaseModel):
    username: str
    password: str
