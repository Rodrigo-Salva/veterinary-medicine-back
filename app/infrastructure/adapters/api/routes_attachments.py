from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
import shutil
from datetime import datetime
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models_attachments import AttachmentModel
from pydantic import BaseModel

router = APIRouter(prefix="/attachments", tags=["attachments"])

UPLOAD_DIR = "uploads/medical"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AttachmentResponse(BaseModel):
    id: uuid.UUID
    pet_id: uuid.UUID
    file_path: str
    file_type: str
    description: Optional[str]
    upload_date: datetime

    class Config:
        from_attributes = True

@router.post("/upload", response_model=AttachmentResponse)
async def upload_attachment(
    pet_id: uuid.UUID = Form(...),
    medical_record_id: Optional[uuid.UUID] = Form(None),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Determine file type
    content_type = file.content_type
    file_type = "Other"
    if content_type.startswith("image/"):
        file_type = "Image"
    elif content_type == "application/pdf":
        file_type = "PDF"

    # Save file
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save to DB
    attachment = AttachmentModel(
        pet_id=pet_id,
        medical_record_id=medical_record_id,
        file_path=file_path,
        file_type=file_type,
        description=description
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return attachment

@router.get("/pet/{pet_id}", response_model=List[AttachmentResponse])
def get_pet_attachments(pet_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(AttachmentModel).filter(AttachmentModel.pet_id == pet_id).all()

@router.delete("/{attachment_id}")
def delete_attachment(attachment_id: uuid.UUID, db: Session = Depends(get_db)):
    attachment = db.query(AttachmentModel).filter(AttachmentModel.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    # Delete file from disk
    if os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)
    
    db.delete(attachment)
    db.commit()
    return {"message": "Attachment deleted successfully"}
