from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import SessionLocal, engine, Base
from app.infrastructure.adapters.db.models import OwnerModel, PetModel, AppointmentModel
from app.infrastructure.adapters.db.models_user import UserModel
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel
from app.infrastructure.adapters.db.models_hospital import CageModel, HospitalizationModel
from app.infrastructure.adapters.db.models_inventory import ProductModel
from app.infrastructure.adapters.api.auth import get_password_hash
import uuid
from datetime import datetime, timedelta

def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 1. Seed Users
        if not db.query(UserModel).filter(UserModel.username == "admin").first():
            admin = UserModel(
                id=uuid.uuid4(),
                username="admin",
                email="admin@vetpremium.com",
                hashed_password=get_password_hash("adminpassword123"),
                role="Admin",
                is_active=True
            )
            db.add(admin)
        
        if not db.query(UserModel).filter(UserModel.username == "vet1").first():
            vet = UserModel(
                id=uuid.uuid4(),
                username="vet1",
                email="doctor@vetpremium.com",
                hashed_password=get_password_hash("vet123"),
                role="Vet",
                is_active=True
            )
            db.add(vet)

        if not db.query(UserModel).filter(UserModel.username == "recepcion1").first():
            recep = UserModel(
                id=uuid.uuid4(),
                username="recepcion1",
                email="recep@vetpremium.com",
                hashed_password=get_password_hash("recep123"),
                role="Receptionist",
                is_active=True
            )
            db.add(recep)

        # 2. Seed Owners
        owner_ids = []
        if db.query(OwnerModel).count() == 0:
            owners_data = [
                {"first_name": "Juan", "last_name": "Perez", "email": "juan@example.com", "phone": "123456789"},
                {"first_name": "Maria", "last_name": "Garcia", "email": "maria@example.com", "phone": "987654321"},
                {"first_name": "Carlos", "last_name": "Rodriguez", "email": "carlos@example.com", "phone": "555123456"}
            ]
            for o_data in owners_data:
                o = OwnerModel(id=uuid.uuid4(), **o_data)
                db.add(o)
                owner_ids.append(o.id)
            db.commit()
        else:
            owner_ids = [o.id for o in db.query(OwnerModel).all()]

        # 3. Seed Pets
        pet_ids = []
        if db.query(PetModel).count() == 0:
            pets_data = [
                {"name": "Max", "species": "Canino", "breed": "Golden Retriever", "age": 3, "owner_id": owner_ids[0]},
                {"name": "Luna", "species": "Felino", "breed": "Siames", "age": 2, "owner_id": owner_ids[1]},
                {"name": "Rocky", "species": "Canino", "breed": "Bulldog", "age": 5, "owner_id": owner_ids[0]},
                {"name": "Bella", "species": "Canino", "breed": "Poodle", "age": 1, "owner_id": owner_ids[2]}
            ]
            for p_data in pets_data:
                p = PetModel(id=uuid.uuid4(), **p_data)
                db.add(p)
                pet_ids.append(p.id)
            db.commit()
        else:
            pet_ids = [p.id for p in db.query(PetModel).all()]

        # 4. Seed Cages
        if db.query(CageModel).count() == 0:
            cages_data = ["A-01", "A-02", "B-01", "B-02", "Hospital-VIP"]
            for name in cages_data:
                c = CageModel(id=uuid.uuid4(), name=name, is_occupied=False)
                db.add(c)

        # 5. Seed Products
        if db.query(ProductModel).count() == 0:
            products_data = [
                {"name": "Vacuna Antirrábica", "category": "Medicina", "purchase_price": 5.0, "sale_price": 15.0, "stock": 50},
                {"name": "Alimento Premium 10kg", "category": "Alimento", "purchase_price": 20.0, "sale_price": 45.0, "stock": 20},
                {"name": "Antiparasitario", "category": "Medicina", "purchase_price": 3.0, "sale_price": 10.0, "stock": 100}
            ]
            for prod_data in products_data:
                prod = ProductModel(id=uuid.uuid4(), **prod_data)
                db.add(prod)

        db.commit()
        print("Database seeded successfully with all types of data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
