from pydantic import BaseModel
from typing import Optional, List
import uuid

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    purchase_price: float
    sale_price: float
    stock: int
    category: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    quantity: int
