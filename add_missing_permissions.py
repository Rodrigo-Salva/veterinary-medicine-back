import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection URL
# Adjust this to your actual database URL
DATABASE_URL = "postgresql://postgres:28demarzo@localhost:5432/veterinaria"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_permissions():
    session = SessionLocal()
    try:
        # 1. Define new permissions
        new_permissions = [
            # Laboratorio
            ("laboratorio", "listar"),
            ("laboratorio", "registrar"),
            ("laboratorio", "editar"),
            ("laboratorio", "eliminar"),
            # Telemedicina
            ("telemedicina", "listar"),
            ("telemedicina", "registrar"),
            ("telemedicina", "editar"),
            ("telemedicina", "eliminar"),
        ]

        # 2. Get Admin role ID
        admin_role = session.execute(text("SELECT id FROM roles WHERE name = 'Admin'")).fetchone()
        if not admin_role:
            print("Error: Role 'Admin' not found.")
            return
        
        admin_id = admin_role[0]

        for module, action in new_permissions:
            # Check if permission exists
            existing = session.execute(
                text("SELECT id FROM permissions WHERE module = :m AND action = :a"),
                {"m": module, "a": action}
            ).fetchone()

            if not existing:
                perm_id = uuid.uuid4()
                session.execute(
                    text("INSERT INTO permissions (id, module, action) VALUES (:id, :m, :a)"),
                    {"id": perm_id, "m": module, "a": action}
                )
                print(f"Added permission: {module} - {action}")
            else:
                perm_id = existing[0]
            
            # Assign to Admin if not already assigned
            assignment = session.execute(
                text("SELECT 1 FROM role_permissions WHERE role_id = :r AND permission_id = :p"),
                {"r": admin_id, "p": perm_id}
            ).fetchone()

            if not assignment:
                session.execute(
                    text("INSERT INTO role_permissions (id, role_id, permission_id) VALUES (:id, :r, :p)"),
                    {"id": uuid.uuid4(), "r": admin_id, "p": perm_id}
                )
                print(f"Assigned {module}:{action} to Admin")

        session.commit()
        print("Successfully updated permissions.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    add_permissions()
