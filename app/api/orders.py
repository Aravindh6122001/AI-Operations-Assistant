from fastapi import APIRouter, Depends , Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse , OrderListResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.create_order(
        db,
        order
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

@router.get("/", response_model=OrderListResponse)
def get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int | None = Query(None),
    status: str | None = Query(None),
    sort_by: str = Query("id"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
):
    return order_service.get_orders(
        db=db,
        page=page,
        page_size=page_size,
        user_id=user_id,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    