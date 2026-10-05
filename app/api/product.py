from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.products import ProductCreate, ProductResponse
from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# POST a product
@router.post(
    "/",
    response_model=ProductResponse
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return product_service.create_product(
        db,
        product.name,
        product.price,
        product.stock
    )


# GET all products
@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):
    return product_service.get_products(db)

# GET a product by ID
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):
    return product_service.get_product_by_id(db,product_id)