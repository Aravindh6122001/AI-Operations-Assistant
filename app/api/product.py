from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product import Product
from app.schemas.products import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product