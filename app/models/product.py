from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint


from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Float)
    
    stock: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )
    
    __table_args__ = (       
         CheckConstraint("price >= 0", name="check_product_price_positive"),
         CheckConstraint("stock >= 0", name="check_product_stock_positive"),
    )