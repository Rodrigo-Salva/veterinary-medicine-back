from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models import PetModel, OwnerModel, AppointmentModel
from app.infrastructure.adapters.api.auth import get_current_user
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter(prefix="/stats", tags=["stats"], dependencies=[Depends(get_current_user)])

@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total_pets = db.query(PetModel).count()
    total_owners = db.query(OwnerModel).count()
    total_appointments = db.query(AppointmentModel).count()
    total_revenue = db.query(func.sum(AppointmentModel.cost)).scalar() or 0.0
    
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

@router.get("/monthly")
def get_monthly_stats(db: Session = Depends(get_db)):
    """Returns appointments count and revenue per month for the last 12 months."""
    results = []
    now = datetime.utcnow()
    for i in range(11, -1, -1):
        # Calculate month boundaries
        month_start = (now.replace(day=1) - timedelta(days=i * 28)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        count = db.query(func.count(AppointmentModel.id)).filter(
            AppointmentModel.date >= month_start,
            AppointmentModel.date < month_end
        ).scalar() or 0

        revenue = db.query(func.sum(AppointmentModel.cost)).filter(
            AppointmentModel.date >= month_start,
            AppointmentModel.date < month_end
        ).scalar() or 0.0

        results.append({
            "month": month_start.strftime("%b %Y"),
            "appointments": count,
            "revenue": round(float(revenue), 2)
        })

    return results

@router.get("/species")
def get_species_stats(db: Session = Depends(get_db)):
    """Returns count of pets grouped by species."""
    rows = db.query(PetModel.species, func.count(PetModel.id)).group_by(PetModel.species).all()
    return [{"species": r[0], "count": r[1]} for r in rows]

@router.get("/top-owners")
def get_top_owners(db: Session = Depends(get_db)):
    """Returns top 5 owners by number of pets."""
    rows = (
        db.query(OwnerModel, func.count(PetModel.id).label("pet_count"))
        .join(PetModel, PetModel.owner_id == OwnerModel.id)
        .group_by(OwnerModel.id)
        .order_by(func.count(PetModel.id).desc())
        .limit(5)
        .all()
    )
    return [
        {
            "owner": f"{r[0].first_name} {r[0].last_name}",
            "email": r[0].email,
            "pet_count": r[1]
        }
        for r in rows
    ]
