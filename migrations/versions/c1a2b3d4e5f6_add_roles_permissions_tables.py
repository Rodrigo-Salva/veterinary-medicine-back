"""add roles and permissions tables, migrate users.role to role_id

Revision ID: c1a2b3d4e5f6
Revises: 0b5f5a90b90a
Create Date: 2026-03-26
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, None] = '0b5f5a90b90a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Pre-defined UUIDs for default roles so we can reference them
ADMIN_ROLE_ID = uuid.UUID('a0000000-0000-0000-0000-000000000001')
VET_ROLE_ID = uuid.UUID('a0000000-0000-0000-0000-000000000002')
RECEPTIONIST_ROLE_ID = uuid.UUID('a0000000-0000-0000-0000-000000000003')

ROLE_MAP = {
    'Admin': ADMIN_ROLE_ID,
    'Vet': VET_ROLE_ID,
    'Receptionist': RECEPTIONIST_ROLE_ID,
}

MODULES = [
    'dashboard', 'mascotas', 'propietarios', 'citas', 'historial_medico',
    'hospitalizacion', 'inventario', 'facturacion', 'reportes', 'usuarios', 'roles',
]
ACTIONS = ['listar', 'registrar', 'editar', 'eliminar']


def upgrade() -> None:
    # 1. Create roles table
    op.create_table(
        'roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('description', sa.String(200), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
    )

    # 2. Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('module', sa.String(50), nullable=False, index=True),
        sa.Column('action', sa.String(20), nullable=False),
        sa.UniqueConstraint('module', 'action', name='uq_permission_module_action'),
    )

    # 3. Create role_permissions table
    op.create_table(
        'role_permissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('role_id', UUID(as_uuid=True), sa.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('permission_id', UUID(as_uuid=True), sa.ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False),
        sa.UniqueConstraint('role_id', 'permission_id', name='uq_role_permission'),
    )

    # 4. Insert default roles
    roles_table = sa.table('roles',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('name', sa.String),
        sa.column('description', sa.String),
        sa.column('is_active', sa.Boolean),
    )
    op.bulk_insert(roles_table, [
        {'id': ADMIN_ROLE_ID, 'name': 'Admin', 'description': 'Administrador con acceso total', 'is_active': True},
        {'id': VET_ROLE_ID, 'name': 'Vet', 'description': 'Veterinario', 'is_active': True},
        {'id': RECEPTIONIST_ROLE_ID, 'name': 'Receptionist', 'description': 'Recepcionista', 'is_active': True},
    ])

    # 5. Insert all permissions
    permissions_table = sa.table('permissions',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('module', sa.String),
        sa.column('action', sa.String),
    )
    permissions = []
    permission_ids = {}
    for module in MODULES:
        for action in ACTIONS:
            pid = uuid.uuid4()
            permission_ids[(module, action)] = pid
            permissions.append({'id': pid, 'module': module, 'action': action})
    op.bulk_insert(permissions_table, permissions)

    # 6. Assign ALL permissions to Admin
    role_perms_table = sa.table('role_permissions',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('role_id', UUID(as_uuid=True)),
        sa.column('permission_id', UUID(as_uuid=True)),
    )
    admin_perms = [
        {'id': uuid.uuid4(), 'role_id': ADMIN_ROLE_ID, 'permission_id': pid}
        for pid in permission_ids.values()
    ]
    op.bulk_insert(role_perms_table, admin_perms)

    # 7. Assign Vet permissions (everything except usuarios and roles management)
    vet_modules = ['dashboard', 'mascotas', 'propietarios', 'citas', 'historial_medico',
                   'hospitalizacion', 'inventario', 'facturacion', 'reportes']
    vet_perms = [
        {'id': uuid.uuid4(), 'role_id': VET_ROLE_ID, 'permission_id': permission_ids[(m, a)]}
        for m in vet_modules for a in ACTIONS
    ]
    op.bulk_insert(role_perms_table, vet_perms)

    # 8. Assign Receptionist permissions (limited)
    recep_perms_def = {
        'dashboard': ['listar'],
        'mascotas': ['listar', 'registrar'],
        'propietarios': ['listar', 'registrar', 'editar'],
        'citas': ['listar', 'registrar', 'editar', 'eliminar'],
        'historial_medico': ['listar'],
        'facturacion': ['listar', 'registrar'],
    }
    recep_perms = [
        {'id': uuid.uuid4(), 'role_id': RECEPTIONIST_ROLE_ID, 'permission_id': permission_ids[(m, a)]}
        for m, actions in recep_perms_def.items() for a in actions
    ]
    op.bulk_insert(role_perms_table, recep_perms)

    # 9. Add role_id column to users (nullable first for migration)
    op.add_column('users', sa.Column('role_id', UUID(as_uuid=True), sa.ForeignKey('roles.id'), nullable=True))

    # 10. Migrate existing users: map role string to role_id
    for role_name, role_id in ROLE_MAP.items():
        op.execute(
            sa.text(f"UPDATE users SET role_id = :role_id WHERE role = :role_name")
            .bindparams(role_id=role_id, role_name=role_name)
        )
    # Default any unmapped users to Vet
    op.execute(
        sa.text("UPDATE users SET role_id = :role_id WHERE role_id IS NULL")
        .bindparams(role_id=VET_ROLE_ID)
    )

    # 11. Make role_id NOT NULL and drop old role column
    op.alter_column('users', 'role_id', nullable=False)
    op.drop_column('users', 'role')


def downgrade() -> None:
    # Re-add role string column
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))

    # Map role_id back to role string
    for role_name, role_id in ROLE_MAP.items():
        op.execute(
            sa.text(f"UPDATE users SET role = :role_name WHERE role_id = :role_id")
            .bindparams(role_name=role_name, role_id=role_id)
        )
    op.execute(
        sa.text("UPDATE users SET role = 'Vet' WHERE role IS NULL")
    )
    op.alter_column('users', 'role', nullable=False)
    op.drop_column('users', 'role_id')

    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')
