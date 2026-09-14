from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.product import Product


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True
    )

    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped["Order"] = relationship(
        back_populates="items"
    )