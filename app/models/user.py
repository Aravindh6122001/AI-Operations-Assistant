from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(String)

    role: Mapped[str] = mapped_column(
        String,
        default="user",
        index=True
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )