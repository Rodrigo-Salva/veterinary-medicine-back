from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import SessionLocal, engine, Base
from app.infrastructure.adapters.db.user_repository_impl import SqlAlchemyUserRepository
from app.infrastructure.adapters.db.role_repository_impl import SqlAlchemyRoleRepository
from app.application.services.user_service import UserService


def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    user_repo = SqlAlchemyUserRepository(db)
    role_repo = SqlAlchemyRoleRepository(db)
    user_service = UserService(user_repo)

    # Get Admin role
    admin_role = role_repo.find_by_name("Admin")
    if not admin_role:
        print("Error: El rol 'Admin' no existe. Ejecuta primero la migración.")
        db.close()
        return

    # Check if admin user already exists
    if not user_service.get_user_by_username("admin"):
        print("Creando usuario admin...")
        user_service.register_user(
            username="admin",
            email="admin@veterinaria.com",
            password="adminpassword123",
            role_id=admin_role.id,
        )
        print("Usuario admin creado exitosamente!")
    else:
        print("El usuario admin ya existe.")

    db.close()


if __name__ == "__main__":
    seed()
