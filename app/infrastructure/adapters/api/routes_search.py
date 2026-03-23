from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models import PetModel, OwnerModel, AppointmentModel

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
def global_search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    term = f"%{q.lower()}%"

    pets = db.query(PetModel).filter(
        (PetModel.name.ilike(term)) | (PetModel.species.ilike(term)) | (PetModel.breed.ilike(term))
    ).limit(5).all()

    owners = db.query(OwnerModel).filter(
        (OwnerModel.first_name.ilike(term)) |
        (OwnerModel.last_name.ilike(term)) |
        (OwnerModel.email.ilike(term))
    ).limit(5).all()

    appointments = db.query(AppointmentModel).filter(
        AppointmentModel.reason.ilike(term)
    ).order_by(AppointmentModel.date.desc()).limit(5).all()

    return {
        "pets": [
            {"id": str(p.id), "name": p.name, "species": p.species, "breed": p.breed}
            for p in pets
        ],
        "owners": [
            {"id": str(o.id), "name": f"{o.first_name} {o.last_name}", "email": o.email, "phone": o.phone}
            for o in owners
        ],
        "appointments": [
            {"id": str(a.id), "reason": a.reason, "date": a.date.isoformat(), "status": a.status}
            for a in appointments
        ]
    }
