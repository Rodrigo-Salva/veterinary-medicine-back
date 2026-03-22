from dataclasses import dataclass
from uuid import UUID, uuid4
from typing import Optional

@dataclass
class Product:
    id: UUID
    name: str
    description: str
    purchase_price: float
    sale_price: float
    stock: int
    category: str  # e.g., "Medicine", "Food", "Supply"

    @classmethod
    def create(cls, name: str, description: str, purchase_price: float, sale_price: float, stock: int, category: str, id: Optional[UUID] = None):
        return cls(
            id=id or uuid4(),
            name=name,
            description=description,
            purchase_price=purchase_price,
            sale_price=sale_price,
            stock=stock,
            category=category
        )
