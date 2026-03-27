from pydantic import BaseModel
from typing import Optional, List
import uuid


class PermissionResponse(BaseModel):
    id: uuid.UUID
    module: str
    action: str

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    is_active: bool
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True


class SetPermissionsRequest(BaseModel):
    permission_ids: List[uuid.UUID]
