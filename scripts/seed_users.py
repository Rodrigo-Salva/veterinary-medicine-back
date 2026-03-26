from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import SessionLocal, engine, Base
from app.infrastructure.adapters.db.user_repository_impl import SqlAlchemyUserRepository
from app.application.services.user_service import UserService
import os

def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    user_repo = SqlAlchemyUserRepository(db)
    user_service = UserService(user_repo)
    
    # Check if admin already exists
    if not user_service.get_user_by_username("admin"):
        print("Seeding initial admin user...")
        user_service.register_user(
            username="admin",
            email="admin@veterinaria.com",
            password="adminpassword123",
            role="Admin"
        )
        print("Admin user created successfully!")
    else:
        print("Admin user already exists.")
    
    db.close()

if __name__ == "__main__":
    seed()
