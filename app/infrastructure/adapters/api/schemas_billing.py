from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class InvoiceItemCreate(BaseModel):
    description: str
    quantity: float = 1.0
    unit_price: float


class InvoiceCreate(BaseModel):
    pet_id: uuid.UUID
    owner_id: uuid.UUID
    items: List[InvoiceItemCreate]
    tax_rate: float = 0.0
    notes: Optional[str] = None


class InvoiceItemResponse(BaseModel):
    id: uuid.UUID
    invoice_id: uuid.UUID
    description: str
    quantity: float
    unit_price: float
    total: float

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: uuid.UUID
    pet_id: uuid.UUID
    owner_id: uuid.UUID
    date: datetime
    subtotal: float
    tax_rate: float
    total: float
    status: str
    notes: Optional[str]
    items: List[InvoiceItemResponse] = []

    class Config:
        from_attributes = True
