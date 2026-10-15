from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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

def update_product(db: Session, product_id: int, update_data: dict):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        return None

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product



def delete_product(db: Session, product_id: int):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        return False

    try:
        db.delete(product)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise