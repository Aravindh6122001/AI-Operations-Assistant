from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories import product_repository


def create_product(
    db: Session,
    name: str,
    price: float,
    stock:int
) -> Product:

    product = Product(
        name=name,
        price=price,
        stock=stock
    )

    return product_repository.create_product(
        db,
        product
    )


def get_products(
    db: Session
) -> list[Product]:

    return product_repository.get_products(db)

def get_product_by_id(
    db: Session,
    product_id: int
) -> list[Product]:

    return product_repository.get_product_by_id(db,product_id)



