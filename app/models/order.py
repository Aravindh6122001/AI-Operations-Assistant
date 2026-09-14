from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="orders"
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )