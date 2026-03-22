from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.product import Product
from app.domain.ports.product_repository import ProductRepository
from app.infrastructure.adapters.db.models_inventory import ProductModel

class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, product: Product) -> Product:
        product_model = ProductModel(
            id=product.id,
            name=product.name,
            description=product.description,
            purchase_price=product.purchase_price,
            sale_price=product.sale_price,
            stock=product.stock,
            category=product.category
        )
        self.db.merge(product_model)
        self.db.commit()
        # To return the refreshed entity, we need to fetch it since merge doesn't refresh the object in place the same way add does
        updated_model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        return self._to_entity(updated_model)

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product_model:
            return self._to_entity(product_model)
        return None

    def get_all(self) -> List[Product]:
        product_models = self.db.query(ProductModel).all()
        return [self._to_entity(pm) for pm in product_models]

    def update_stock(self, product_id: UUID, quantity: int) -> Product:
        product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product_model:
            raise Exception("Product not found")
        
        product_model.stock += quantity
        self.db.commit()
        self.db.refresh(product_model)
        return self._to_entity(product_model)

    def delete(self, product_id: UUID) -> bool:
        product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product_model:
            self.db.delete(product_model)
            self.db.commit()
            return True
        return False

    def _to_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            purchase_price=model.purchase_price,
            sale_price=model.sale_price,
            stock=model.stock,
            category=model.category
        )
