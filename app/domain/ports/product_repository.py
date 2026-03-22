from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def update_stock(self, product_id: UUID, quantity: int) -> Product:
        pass

    @abstractmethod
    def delete(self, product_id: UUID) -> bool:
        pass
