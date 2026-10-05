import math

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories import order_repository

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

def get_user_orders(
    db: Session,
    user_id: int
) -> list[Order]:

    return order_repository.get_orders_by_user(
        db,
        user_id
    )


def create_order(db: Session, order_data):
    try:
        order = Order(
            user_id=order_data.user_id,
            status="pending"
        )

        db.add(order)
        db.flush()

        for item in order_data.items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found"
                )

            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {product.id}"
                )

            product.stock -= item.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity
            )

            db.add(order_item)

        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise

def get_orders(
    db: Session,
    page: int,
    page_size: int,
    user_id: int | None = None,
    status: str | None = None,
    sort_by: str = "id",
    sort_order: str = "desc",
):
    orders, total = order_repository.get_orders(
        db=db,
        page=page,
        page_size=page_size,
        user_id=user_id,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    total_pages = math.ceil(total / page_size) if total else 0

    return {
        "items": orders,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }    