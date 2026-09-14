from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories import order_repository

from app.models.order import Order
from app.repositories import order_repository


def get_user_orders(db: Session, user_id: int) -> list[Order]:
    return order_repository.get_orders_by_user(db, user_id)


def create_order(
    db: Session,
    user_id: int,
    items: list
) -> Order:

    order = Order(user_id=user_id)

    for item in items:
        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity
        )

        order.items.append(order_item)

    return order_repository.create_order(db, order)