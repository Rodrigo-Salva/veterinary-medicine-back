"""
Script para migrar la BD al nuevo sistema de roles y permisos.
Ejecutar: python migrate_roles.py
"""
import uuid
from sqlalchemy import create_engine, text
from app.infrastructure.config.settings import settings

engine = create_engine(settings.DATABASE_URL)

ADMIN_ROLE_ID = uuid.UUID('a0000000-0000-0000-0000-000000000001')
VET_ROLE_ID = uuid.UUID('a0000000-0000-0000-0000-000000000002')
RECEPTIONIST_ROLE_ID = uuid.UUID('a0000000-0000-0000-0000-000000000003')

MODULES = [
    'dashboard', 'mascotas', 'propietarios', 'citas', 'historial_medico',
    'hospitalizacion', 'inventario', 'facturacion', 'reportes', 'usuarios', 'roles',
]
ACTIONS = ['listar', 'registrar', 'editar', 'eliminar']


def migrate():
    with engine.begin() as conn:
        # 1. Crear tabla roles
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS roles (
                id UUID PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                description VARCHAR(200),
                is_active BOOLEAN DEFAULT TRUE
            )
        """))
        print("Tabla 'roles' creada.")

        # 2. Crear tabla permissions
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS permissions (
                id UUID PRIMARY KEY,
                module VARCHAR(50) NOT NULL,
                action VARCHAR(20) NOT NULL,
                CONSTRAINT uq_permission_module_action UNIQUE (module, action)
            )
        """))
        print("Tabla 'permissions' creada.")

        # 3. Crear tabla role_permissions
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS role_permissions (
                id UUID PRIMARY KEY,
                role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
                permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
                CONSTRAINT uq_role_permission UNIQUE (role_id, permission_id)
            )
        """))
        print("Tabla 'role_permissions' creada.")

        # 4. Insertar roles por defecto (si no existen)
        roles_data = [
            (ADMIN_ROLE_ID, 'Admin', 'Administrador con acceso total'),
            (VET_ROLE_ID, 'Vet', 'Veterinario'),
            (RECEPTIONIST_ROLE_ID, 'Receptionist', 'Recepcionista'),
        ]
        for rid, name, desc in roles_data:
            exists = conn.execute(text("SELECT 1 FROM roles WHERE id = :id"), {"id": rid}).fetchone()
            if not exists:
                conn.execute(text(
                    "INSERT INTO roles (id, name, description, is_active) VALUES (:id, :name, :desc, TRUE)"
                ), {"id": rid, "name": name, "desc": desc})
                print(f"  Rol '{name}' insertado.")
            else:
                print(f"  Rol '{name}' ya existe.")

        # 5. Insertar todos los permisos
        permission_ids = {}
        for module in MODULES:
            for action in ACTIONS:
                exists = conn.execute(text(
                    "SELECT id FROM permissions WHERE module = :m AND action = :a"
                ), {"m": module, "a": action}).fetchone()
                if exists:
                    permission_ids[(module, action)] = exists[0]
                else:
                    pid = uuid.uuid4()
                    conn.execute(text(
                        "INSERT INTO permissions (id, module, action) VALUES (:id, :m, :a)"
                    ), {"id": pid, "m": module, "a": action})
                    permission_ids[(module, action)] = pid
        print(f"  {len(permission_ids)} permisos insertados/verificados.")

        # 6. Asignar TODOS los permisos al Admin
        for pid in permission_ids.values():
            exists = conn.execute(text(
                "SELECT 1 FROM role_permissions WHERE role_id = :rid AND permission_id = :pid"
            ), {"rid": ADMIN_ROLE_ID, "pid": pid}).fetchone()
            if not exists:
                conn.execute(text(
                    "INSERT INTO role_permissions (id, role_id, permission_id) VALUES (:id, :rid, :pid)"
                ), {"id": uuid.uuid4(), "rid": ADMIN_ROLE_ID, "pid": pid})
        print("  Permisos de Admin asignados (todos).")

        # 7. Asignar permisos de Vet
        vet_modules = ['dashboard', 'mascotas', 'propietarios', 'citas', 'historial_medico',
                       'hospitalizacion', 'inventario', 'facturacion', 'reportes']
        for module in vet_modules:
            for action in ACTIONS:
                pid = permission_ids[(module, action)]
                exists = conn.execute(text(
                    "SELECT 1 FROM role_permissions WHERE role_id = :rid AND permission_id = :pid"
                ), {"rid": VET_ROLE_ID, "pid": pid}).fetchone()
                if not exists:
                    conn.execute(text(
                        "INSERT INTO role_permissions (id, role_id, permission_id) VALUES (:id, :rid, :pid)"
                    ), {"id": uuid.uuid4(), "rid": VET_ROLE_ID, "pid": pid})
        print("  Permisos de Vet asignados.")

        # 8. Asignar permisos de Receptionist
        recep_perms = {
            'dashboard': ['listar'],
            'mascotas': ['listar', 'registrar'],
            'propietarios': ['listar', 'registrar', 'editar'],
            'citas': ['listar', 'registrar', 'editar', 'eliminar'],
            'historial_medico': ['listar'],
            'facturacion': ['listar', 'registrar'],
        }
        for module, actions in recep_perms.items():
            for action in actions:
                pid = permission_ids[(module, action)]
                exists = conn.execute(text(
                    "SELECT 1 FROM role_permissions WHERE role_id = :rid AND permission_id = :pid"
                ), {"rid": RECEPTIONIST_ROLE_ID, "pid": pid}).fetchone()
                if not exists:
                    conn.execute(text(
                        "INSERT INTO role_permissions (id, role_id, permission_id) VALUES (:id, :rid, :pid)"
                    ), {"id": uuid.uuid4(), "rid": RECEPTIONIST_ROLE_ID, "pid": pid})
        print("  Permisos de Receptionist asignados.")

        # 9. Agregar columna role_id a users (si no existe)
        col_exists = conn.execute(text("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name = 'users' AND column_name = 'role_id'
        """)).fetchone()

        if not col_exists:
            conn.execute(text("ALTER TABLE users ADD COLUMN role_id UUID"))
            print("  Columna 'role_id' agregada a users.")

            # 10. Migrar datos: role string -> role_id
            role_map = {'Admin': ADMIN_ROLE_ID, 'Vet': VET_ROLE_ID, 'Receptionist': RECEPTIONIST_ROLE_ID}
            for role_name, role_id in role_map.items():
                conn.execute(text(
                    "UPDATE users SET role_id = :role_id WHERE role = :role_name"
                ), {"role_id": role_id, "role_name": role_name})
            # Usuarios sin mapear -> Vet
            conn.execute(text(
                "UPDATE users SET role_id = :role_id WHERE role_id IS NULL"
            ), {"role_id": VET_ROLE_ID})
            print("  Datos migrados de role -> role_id.")

            # 11. Hacer role_id NOT NULL y FK
            conn.execute(text("ALTER TABLE users ALTER COLUMN role_id SET NOT NULL"))
            conn.execute(text(
                "ALTER TABLE users ADD CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id)"
            ))
            print("  Restriccion NOT NULL y FK agregadas.")

            # 12. Eliminar columna role vieja
            conn.execute(text("ALTER TABLE users DROP COLUMN role"))
            print("  Columna 'role' (string) eliminada.")
        else:
            print("  Columna 'role_id' ya existe, no se necesita migrar.")

        # 13. Actualizar alembic_version para que alembic no intente re-ejecutar
        alembic_exists = conn.execute(text(
            "SELECT 1 FROM information_schema.tables WHERE table_name = 'alembic_version'"
        )).fetchone()
        if alembic_exists:
            conn.execute(text("DELETE FROM alembic_version"))
            conn.execute(text(
                "INSERT INTO alembic_version (version_num) VALUES ('c1a2b3d4e5f6')"
            ))
            print("  alembic_version actualizado a 'c1a2b3d4e5f6'.")

    print("\n¡Migracion completada exitosamente!")


if __name__ == "__main__":
    migrate()
