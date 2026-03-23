from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.adapters.db.database import Base
import uuid
from datetime import datetime

class InvoiceModel(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    subtotal = Column(Float, nullable=False, default=0.0)
    tax_rate = Column(Float, nullable=False, default=0.0)  # percentage e.g. 19.0
    total = Column(Float, nullable=False, default=0.0)
    status = Column(String, nullable=False, default="Pending")  # Pending / Paid / Cancelled
    notes = Column(Text, nullable=True)

class InvoiceItemModel(Base):
    __tablename__ = "invoice_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    unit_price = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
