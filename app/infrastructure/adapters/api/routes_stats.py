from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models import PetModel, OwnerModel, AppointmentModel
from sqlalchemy import func

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total_pets = db.query(PetModel).count()
    total_owners = db.query(OwnerModel).count()
    total_appointments = db.query(AppointmentModel).count()
    total_revenue = db.query(func.sum(AppointmentModel.cost)).scalar() or 0.0
    
    # Recent appointments for the right panel
    recent_appointments = db.query(AppointmentModel).order_by(AppointmentModel.date.desc()).limit(5).all()
    
    return {
        "total_pets": total_pets,
        "total_owners": total_owners,
        "total_appointments": total_appointments,
        "total_revenue": total_revenue,
        "recent_activity": [
            {
                "id": str(a.id),
                "reason": a.reason,
                "date": a.date.isoformat(),
                "cost": a.cost,
                "status": a.status
            } for a in recent_appointments
        ]
    }
