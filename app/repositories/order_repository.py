from sqlalchemy.orm import Session

from app.models.order import Order


def create_order(
    db: Session,
    order: Order
) -> Order:

    db.add(order)
    db.flush()

    db.commit()
    db.refresh(order)

    return order


def get_orders_by_user(
    db: Session,
    user_id: int
) -> list[Order]:

    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .all()
    )


def get_orders(
    db: Session,
    page: int,
    page_size: int,
    user_id: int | None = None,
    status: str | None = None,
    sort_by: str = "id",
    sort_order: str = "desc",
):
    query = db.query(Order)

    # Filtering
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)

    if status is not None:
        query = query.filter(Order.status == status)

    # Sorting
    allowed_sort_fields = {
        "id": Order.id,
        "status": Order.status,
    }

    sort_column = allowed_sort_fields.get(sort_by, Order.id)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Total before pagination
    total = query.count()

    # Pagination
    offset = (page - 1) * page_size

    orders = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return orders, total    