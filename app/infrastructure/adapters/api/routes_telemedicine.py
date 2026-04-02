from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
from .schemas_telemedicine import TelemedicineSessionResponse, TelemedicineSessionCreate
from app.infrastructure.adapters.api.auth import permission_required

router = APIRouter(prefix="/telemedicine", tags=["telemedicine"])

# In-memory storage for the demo
sessions_db = {}

@router.post("/sessions", response_model=TelemedicineSessionResponse)
async def create_session(
    session_data: TelemedicineSessionCreate,
    _=Depends(permission_required("telemedicina", "registrar"))
):
    session_id = uuid.uuid4()
    # Mocking room URL generation
    room_url = f"https://meet.jit.si/veterinita-{session_id}"
    
    new_session = {
        "id": session_id,
        "appointment_id": session_data.appointment_id,
        "pet_id": session_data.pet_id,
        "doctor_name": "Dr. Smith", # Placeholder
        "pet_name": "Patient", # Placeholder
        "room_url": room_url,
        "status": "active",
        "start_time": datetime.now()
    }
    sessions_db[str(session_id)] = new_session
    return new_session

@router.get("/sessions", response_model=List[TelemedicineSessionResponse])
async def get_active_sessions(
    _=Depends(permission_required("telemedicina", "listar"))
):
    return list(sessions_db.values())

@router.get("/sessions/{session_id}", response_model=TelemedicineSessionResponse)
async def get_session(
    session_id: uuid.UUID,
    _=Depends(permission_required("telemedicina", "listar"))
):
    session = sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/sessions/{session_id}/end")
async def end_session(
    session_id: uuid.UUID,
    _=Depends(permission_required("telemedicina", "eliminar"))
):
    if str(session_id) in sessions_db:
        sessions_db[str(session_id)]["status"] = "completed"
        sessions_db[str(session_id)]["end_time"] = datetime.now()
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Session not found")
