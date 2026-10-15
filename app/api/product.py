from fastapi import APIRouter, Depends ,  HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from app.db.session import get_db
from app.schemas.products import ProductCreate, ProductResponse ,ProductUpdate
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


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
):
    try:
        product = product_service.update_product(
            db, product_id, product_data
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        deleted = product_service.delete_product(db, product_id)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this product because it is referenced by existing order items.",
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {"message": "Product deleted successfully"}