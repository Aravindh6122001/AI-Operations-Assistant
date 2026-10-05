from sqlalchemy.orm import Session

from app.models.product import Product


def create_product(
    db: Session,
    product: Product
) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_product_by_id(
    db: Session,
    product_id: int
) -> Product | None:
    return db.get(Product, product_id)


def get_products(
    db: Session
) -> list[Product]:
    return db.query(Product).all()