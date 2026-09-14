from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.create_order(
        db,
        order.user_id,
        order.items
    )

@router.get("/user/{user_id}", response_model=list[OrderResponse])
def get_user_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    return order_service.get_user_orders(
        db,
        user_id
    )

    