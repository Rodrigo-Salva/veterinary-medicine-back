from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.models_billing import InvoiceModel, InvoiceItemModel
from app.infrastructure.adapters.api.schemas_billing import InvoiceCreate, InvoiceResponse, InvoiceItemResponse
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/billing", tags=["billing"], dependencies=[Depends(get_current_user)])

# ─── Endpoints ──────────────────────────────────────────────────────────────

@router.post("/", response_model=InvoiceResponse)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db)):
    # Build items and calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in data.items)
    tax_amount = subtotal * (data.tax_rate / 100)
    total = subtotal + tax_amount

    invoice = InvoiceModel(
        pet_id=data.pet_id,
        owner_id=data.owner_id,
        subtotal=round(subtotal, 2),
        tax_rate=data.tax_rate,
        total=round(total, 2),
        notes=data.notes,
        date=datetime.utcnow()
    )
    db.add(invoice)
    db.flush()  # get invoice.id before adding items

    item_models = []
    for item in data.items:
        item_total = item.quantity * item.unit_price
        inv_item = InvoiceItemModel(
            invoice_id=invoice.id,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total=round(item_total, 2)
        )
        db.add(inv_item)
        item_models.append(inv_item)

    db.commit()
    db.refresh(invoice)

    invoice.items = db.query(InvoiceItemModel).filter(InvoiceItemModel.invoice_id == invoice.id).all()
    return invoice

@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(InvoiceModel)
    if status:
        q = q.filter(InvoiceModel.status == status)
    invoices = q.order_by(InvoiceModel.date.desc()).all()
    for inv in invoices:
        inv.items = db.query(InvoiceItemModel).filter(InvoiceItemModel.invoice_id == inv.id).all()
    return invoices

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    invoice = db.query(InvoiceModel).filter(InvoiceModel.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice.items = db.query(InvoiceItemModel).filter(InvoiceItemModel.invoice_id == invoice.id).all()
    return invoice

@router.patch("/{invoice_id}/status")
def update_invoice_status(invoice_id: uuid.UUID, status: str, db: Session = Depends(get_db)):
    if status not in ["Pending", "Paid", "Cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid status. Use: Pending, Paid, Cancelled")
    invoice = db.query(InvoiceModel).filter(InvoiceModel.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice.status = status
    db.commit()
    db.refresh(invoice)
    return {"id": str(invoice.id), "status": invoice.status}

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    invoice = db.query(InvoiceModel).filter(InvoiceModel.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.query(InvoiceItemModel).filter(InvoiceItemModel.invoice_id == invoice_id).delete()
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted"}
