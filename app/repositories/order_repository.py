from sqlalchemy.orm import Session

from app.models.order import Order


def create_order(db: Session, order: Order) -> Order:
    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()

def create_order(db: Session, order: Order) -> Order:
    db.add(order)
    db.flush()

    db.commit()
    db.refresh(order)

    return order