from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))
    email: Mapped[int] = mapped_column(String(100),unique=True,index=True)
    
    orders: Mapped[list["Order"]] = relationship(
        back_populates = "user",
        cascade="all, delete-orphan"
    )
    

 