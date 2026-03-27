from sqlalchemy import Column, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.adapters.db.database import Base
import uuid


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)

    permissions = relationship("RolePermissionModel", back_populates="role", cascade="all, delete-orphan")


class PermissionModel(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module = Column(String(50), nullable=False, index=True)
    action = Column(String(20), nullable=False)

    __table_args__ = (
        UniqueConstraint("module", "action", name="uq_permission_module_action"),
    )


class RolePermissionModel(Base):
    __tablename__ = "role_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    role = relationship("RoleModel", back_populates="permissions")
    permission = relationship("PermissionModel")

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
