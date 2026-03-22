from typing import List, Optional
from uuid import UUID
from app.domain.entities.product import Product
from app.domain.ports.product_repository import ProductRepository

class InventoryUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def add_product(self, name: str, description: str, purchase_price: float, sale_price: float, stock: int, category: str) -> Product:
        product = Product.create(
            name=name,
            description=description,
            purchase_price=purchase_price,
            sale_price=sale_price,
            stock=stock,
            category=category
        )
        return self.repository.save(product)

    def get_inventory(self) -> List[Product]:
        return self.repository.get_all()

    def get_product(self, product_id: UUID) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def update_product(self, product_id: UUID, name: str, description: str, purchase_price: float, sale_price: float, stock: int, category: str) -> Product:
        product = Product(
            id=product_id,
            name=name,
            description=description,
            purchase_price=purchase_price,
            sale_price=sale_price,
            stock=stock,
            category=category
        )
        return self.repository.save(product) # SqlAlchemy 'merge' or 'add' with existing ID needs investigation

    def update_stock(self, product_id: UUID, quantity: int) -> Product:
        return self.repository.update_stock(product_id, quantity)

    def delete_product(self, product_id: UUID) -> bool:
        return self.repository.delete(product_id)
