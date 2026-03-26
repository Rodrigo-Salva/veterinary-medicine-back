from app.infrastructure.adapters.db.database import SessionLocal
from app.infrastructure.adapters.db.models import PetModel, OwnerModel, AppointmentModel
from app.infrastructure.adapters.db.models_hospital import CageModel, HospitalizationModel, VitalSignModel
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel
import uuid

def seed_cages():
    db = SessionLocal()
    try:
        cages = [
            "Jaula A1 (Grande)",
            "Jaula A2 (Grande)",
            "Jaula B1 (Mediana)",
            "Jaula B2 (Mediana)",
            "Jaula C1 (Pequeña)",
            "Cucha de Recuperación 1"
        ]
        
        for name in cages:
            existing = db.query(CageModel).filter(CageModel.name == name).first()
            if not existing:
                cage = CageModel(id=uuid.uuid4(), name=name, is_occupied=False)
                db.add(cage)
        
        db.commit()
        print(f"✅ Seeding completed: {len(cages)} cages added/verified.")
    except Exception as e:
        print(f"❌ Error seeding cages: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_cages()
