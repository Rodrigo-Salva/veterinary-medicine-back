from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.infrastructure.adapters.db.database import get_db
from app.infrastructure.adapters.db.product_repository_impl import SqlAlchemyProductRepository
from app.application.services.inventory_service import InventoryUseCase
from app.infrastructure.adapters.api.schemas_inventory import ProductCreate, ProductResponse, StockUpdate
from app.infrastructure.adapters.api.auth import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"], dependencies=[Depends(get_current_user)])

def get_inventory_service(db: Session = Depends(get_db)):
    repository = SqlAlchemyProductRepository(db)
    return InventoryUseCase(repository)

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, service: InventoryUseCase = Depends(get_inventory_service)):
    return service.add_product(
        name=product.name,
        description=product.description,
        purchase_price=product.purchase_price,
        sale_price=product.sale_price,
        stock=product.stock,
        category=product.category
    )

@router.get("/", response_model=List[ProductResponse])
def list_products(service: InventoryUseCase = Depends(get_inventory_service)):
    return service.get_inventory()

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, product: ProductCreate, service: InventoryUseCase = Depends(get_inventory_service)):
    return service.update_product(
        product_id=product_id,
        name=product.name,
        description=product.description,
        purchase_price=product.purchase_price,
        sale_price=product.sale_price,
        stock=product.stock,
        category=product.category
    )

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, service: InventoryUseCase = Depends(get_inventory_service)):
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/{product_id}/stock", response_model=ProductResponse)
def update_stock(product_id: UUID, update: StockUpdate, service: InventoryUseCase = Depends(get_inventory_service)):
    try:
        return service.update_stock(product_id, update.quantity)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: UUID, service: InventoryUseCase = Depends(get_inventory_service)):
    if not service.delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
