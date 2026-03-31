from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models import OwnerModel, PetModel, AppointmentModel
from pydantic import BaseModel

router = APIRouter(prefix="/public", tags=["public"])

class PublicAppointmentRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    pet_name: str
    species: str
    breed: str
    reason: str
    date: datetime

@router.post("/appointments")
async def create_public_appointment(req: PublicAppointmentRequest, db: Session = Depends(get_db)):
    # 1. Find or create owner
    owner = db.query(OwnerModel).filter(OwnerModel.email == req.email).first()
    if not owner:
        owner = OwnerModel(
            first_name=req.first_name,
            last_name=req.last_name,
            email=req.email,
            phone=req.phone
        )
        db.add(owner)
        db.flush() # Get owner.id
    
    # 2. Find or create pet
    pet = db.query(PetModel).filter(PetModel.owner_id == owner.id, PetModel.name == req.pet_name).first()
    if not pet:
        pet = PetModel(
            name=req.pet_name,
            species=req.species,
            breed=req.breed,
            age=0, # Unknown
            owner_id=owner.id,
            notes=f"Registrado via portal público de reservas el {datetime.now().strftime('%Y-%m-%d')}"
        )
        db.add(pet)
        db.flush() # Get pet.id
    
    # 3. Create appointment
    appointment = AppointmentModel(
        pet_id=pet.id,
        owner_id=owner.id,
        date=req.date,
        reason=req.reason,
        status="Pending",
        cost=0.0 # To be determined
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    return {"message": "Reserva recibida correctamente", "appointment_id": str(appointment.id)}
